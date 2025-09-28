def addition(input_list, add_num):
    new_list = []

    for element in input_list:
        new_element = element + add_num 
        new_list.append(new_element)
    return new_list

def power_of_list(input_list, power_num):
    new_list = []
    for element in input_list:
        new_element = element ** power_num
        new_list.append(new_element)
    return new_list