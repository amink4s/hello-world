text = input("please write a text: ")
words = text.split()

longest_word = ""
for word in words:
    if len(word) > len(longest_word):
        longest_word = word
print(f"A) The longest word is: {longest_word}")

letter_count = 0
for char in text:
    if char.isalpha():
        letter_count += 1
print(f"B) Total number of letters: {letter_count}")

average_word_length = letter_count / len(words) if words else 0
print(f"C) Average word length: {average_word_length:.2f}")