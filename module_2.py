import random
import string
from random import randint


dict_count = random.randint(2, 10)    # create random number for dictionaries count in list from 2 to 10
print('Count of dictionaries in source list is: ' + str(dict_count))

n = 2     # set min number for dictionaries count in list
dict_list = []    # declare empty list for dictionaries list
while n <= dict_count + 1:
    # add to dict_list list where element is random number fro 0 to 100, key is random lowercase letter,
    # k = max number of items in each dictionary
    dict_list.append({ele: randint(0, 100) for ele in random.choices(string.ascii_lowercase, k=randint(1, 5))})
    n += 1
print(f'Source list of dictionaries is:')
print(dict_list)

keys_list = []     # declare empty list for all keys of all dictionaries
for element in dict_list:    # for each element in  dict_list
    for key in element.keys():    # for each key of dictionary in dict_list
        keys_list.append(key)    # add this key to keys_list
# print(keys_list)

# create empty dictionary which will store list of values from different dictionaries for common keys
combined_dict = {}
for key in keys_list:    # for each key in keys_list
    combined_dict[key] = []    # declare empty list for each key in keys_list
    for element in dict_list:    # for each list in dict_list
        if key in element.keys():    # if key from keys_list in key of source dictionary
            combined_dict[key].append(element[key])    # add this key and value of the key to combined_dict
        else:
            # add this key and -1 value as indicator to be able find number of dict to combined_dict
            combined_dict[key].append(-1)
# print(combined_dict)

final_dict = {}    # declare final dictionary
i = 0
for key in combined_dict.keys():    # for ach key in combined_dict
    # create short_values_list and remove all values = -1
    short_values_list = [value for value in combined_dict[key] if value != -1]
    # if len of short_values_list = 1 it means that only one value exists for this key and key should not be renamed
    if len(short_values_list) == 1:
        # add key and value to final dictionary
        final_dict[key] = short_values_list[0]
    else:
        # if len of short_values_list != 1 it means that several values exist for this key and key should be renamed
        # and max value should be found
        # find number of dictionary with max value from source dict_list to add to key with _
        key2 = key + '_' + str(combined_dict[key].index(max(combined_dict[key]))+1)
        # add max value for renamed key to final dictionary
        final_dict[key2] = max(combined_dict[key])
        i = i+1

print(f'Final dictionary is:')
print(final_dict)
