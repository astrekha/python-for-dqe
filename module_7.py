import csv
import re


# function to prepare string for count - removes '- 'and ',', replaces '.' in the end of string,
# converses string to lowercase
# returns modified string
def prepare_str(input_str):
    input_str = re.sub(r'[-,:]', '', input_str)
    input_str = input_str.lower().split()
    f_str_modified = []
    for element in input_str:
        if element.endswith('.'):
            element = element.replace('.', '')
        f_str_modified.append(element)
    return f_str_modified


# function to split string by characters
# returns list ow words [character1, character2, ..., characterN]
def split_str_to_char(input_str):
    char_list = []
    for word in input_str:
        for char in word:
            if char.isalpha():
                char_list.append(char)
    return char_list


# function to count words in string
# returns dictionary {unique word: count}
def get_word_count(input_str):
    counts = {}
    for word in input_str:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts


# function to count characters in string (counts both lowercase and uppercase)
# returns dictionary {unique character shown in lowercase: count}
def get_letter_count_full(input_str):
    counts = {}
    for letter in input_str:
        if letter.lower() in counts:
            counts[letter.lower()] += 1
        else:
            counts[letter.lower()] = 1
    return counts


# function to count only uppercase characters in string, if character is in lowercase - set 0 value for it
# returns dictionary {unique character in uppercase: count}
def get_letter_count_upper(input_str):
    counts = {}
    for letter in input_str:
        if letter.isupper():
            if letter in counts:
                counts[letter] += 1
            else:
                counts[letter] = 1
        else:
            if letter.upper() not in counts:
                counts[letter.upper()] = 0
    return counts


# function to write word statistics to csv file
def write_word_statistics(file_path):
    try:
        # open source file with feed
        f = open(file_path, 'r')
        f_str_original = f.read()
        f_str_prepared = prepare_str(f_str_original)
        # get count of each word from prepared string
        word_count = get_word_count(f_str_prepared)
        # write results to csv file
        with open('word_statistics.csv', 'w', newline='') as csv_f:
            wr = csv.writer(csv_f, delimiter='-')
            for key, value in word_count.items():
                wr.writerow([key, value])
    except FileNotFoundError:
        print(f'Incorrect file path: {file_path}')


# function to write letter statistics to csv file
def write_letter_statistics(file_path):
    try:
        # open source file with feed
        f = open(file_path, 'r')
        f_str_original = f.read()
        # get list of all characters
        char_list = split_str_to_char(f_str_original)
        total_letter_count = len(char_list)        # get total count of characters
        letter_count = get_letter_count_full(char_list)    # get count of each character
        letter_count_up = get_letter_count_upper(char_list)    # get count of each uppercase character
        # get percentage of each character
        letter_percentage = {}
        for key in letter_count.keys():
            letter_percentage[key.upper()] = round((letter_count[key]/total_letter_count)*100, 2)
        final_res = []
        final_res.extend([letter_count, letter_count_up, letter_percentage])
        # write results to csv file
        header = ['letter', 'count_all', 'count_uppercase', 'percentage']
        with open('letter_statistics.csv', 'w', newline='') as csv_f:
            wr = csv.writer(csv_f, delimiter=',')
            wr.writerow(header)
            for key, value in letter_count.items():
                wr.writerow([key, value, letter_count_up[key.upper()], letter_percentage[key.upper()]])
    except FileNotFoundError:
        print(f'Incorrect file path: {file_path}')