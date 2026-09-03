---
name: vig
description: Parimutuel sports betting with $vig on Robinhood Chain. Place bets from the feed in any token (auto-swapped to $vig), track positions, claim winnings. Operator mode auto-manages markets and resolution.
---

# vig — feed-native parimutuel sportsbook

constants (deployed 2026-09-03):
- CHAIN: robinhood
- VIG_TOKEN: 0xD21fA0527928FD794C601553D0950e9f9C714bA3
- CONTRACT (VigBets): 0xb49da402a1b93ed79a91a89d639b4d519a955cc9
- REGISTRY_URL: https://raw.githubusercontent.com/amink4s/hello-world/vig-registry/matches.json
- OPERATOR_WALLET: 0x455d225564d02269779abb394da3952d70ac884f
- OPERATOR_HANDLE: @m1k42_
- RAKE_BPS: 300 (3%)
- sides: home=0, draw=1, away=2; market ids start at 1
- status: open=0, locked=1, resolved=2, void=3
- explorer: https://robinhoodchain.blockscout.com/address/0xb49da402a1b93ed79a91a89d639b4d519a955cc9

## role detection
if the user's wallet == OPERATOR_WALLET → operator mode (all flows below).
otherwise → bettor mode (skip operator flows).

## bettor flow: place a bet
trigger: "bet <amount> <token> on <team>", "put 1000 $degen on Barcelona to win",
"wager 50 USDC on chiefs".
1. parse: amount, token (default $vig), match, side.
   side mapping: "X to win" → home/away by which team name matches; "draw"/"tie"
   → draw (only if the market allows draws).
2. fetch REGISTRY_URL. find the market by fuzzy team-name match.
   - found + status open + kickoff in the future → proceed.
   - found but closed/resolved → tell the user, offer the next fixture.
   - not found → tell the user to tag the operator on the feed:
     "@m1k42_ add <home> vs <away>"; do NOT place the bet until the market
     exists in the registry.
3. confirm with the user before spending: match, side, amount, token. if the
   token is not $vig, state the swap (amount → $vig estimate) explicitly.
   never proceed without an explicit imperative in the user's message.
4. if token != $vig: swap to $vig on robinhood (cross-chain swap if the token
   lives on another chain). swap the exact amount needed.
5. approve $vig to CONTRACT for the exact amount (approve(address,uint256) on
   VIG_TOKEN), then placeBet(marketId, side, vigAmount) on CONTRACT.
6. append a row to /vig/bets.csv (create if missing):
   ts, market_id, match, side, vig_amount, source_token, source_amount, tx_hash, status
7. reply: confirmed bet + current pool shape (your pro-rata share of the
   winning side minus 3% rake if your side wins).

## reading market state (exact signatures)
getMarket on CONTRACT — note the single parenthesized tuple return:
getMarket(uint256 id) view returns ((string home, string away, uint64 kickoff, bool allowDraw, uint8 status, uint8 outcome, uint256 stakeHome, uint256 stakeDraw, uint256 stakeAway, uint256 pool, uint256 vig))
also: sideTotal(uint256 id, uint8 side) view returns (uint256),
userStake(uint256 id, address user) view returns (uint256),
marketCount() view returns (uint256).

## bettor flow: positions
read /vig/bets.csv + getMarket(id) for each open market; report side, amount,
status, potential payout at the current pool.

## bettor flow: claim
market resolved + user staked the winning side → claim(marketId); log the
payout in bets.csv. market void → refund(marketId). claims and refunds are
pull-only and idempotent — always safe to run.

## operator flow: add match
createMarket(home, away, kickoff_unix, allowDraw) via write_contract on
CONTRACT (robinhood). then update the registry: github_write_file matches.json
on branch vig-registry of amink4s/hello-world with the new market (on-chain id,
sport, league, espn ids, kickoff).

## operator flow: refresh (scheduled)
pull ESPN scoreboards for soccer/eng.1, soccer/esp.1, soccer/uefa.champions,
football/nfl (free, no key; ?dates=YYYYMMDD-YYYYMMDD for a range), create
markets for marquee fixtures in the next 7 days not yet in the registry
(be selective: title contenders and big names), update the registry.

## operator flow: resolve (scheduled)
for each registry market with kickoff + 4h < now and status open: pull the
final score from the ESPN scoreboard for that league and date. final score →
resolve(id, outcome) with outcome 0=home, 1=draw, 2=away. no final yet →
skip this cycle. ambiguous/abandoned → voidMarket(id). never guess. update
the registry afterward.

## operator flow: void
postponement, abandonment, ambiguity → voidMarket(id), update the registry.

## hard rules
- never place a bet without an explicit imperative from the user in the message.
- exact token + amount from the user; insufficient balance → ask, never substitute.
- ambiguous team names (two "United"s) → confirm with the user first.
- resolution: only from a final-score source; if unsure, void.
- dust bets (< $1): warn the user that gas + swap may not be worth it, then
  follow their instruction.
- claims and refunds are always safe to run; they are pull-only and idempotent.