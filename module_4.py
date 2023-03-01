import re
import random
import string
from random import randint


# part for module 2
def create_dict_list(num):
    """
    function for creation list of dictionaries with number of elements from 2 till num
    :param num: int
    :return: list of dictionaries
    """
    dict_count = random.randint(2, num)  # create random number for dictionaries count in list from 2 to 10
    n = 2  # set min number for dictionaries count in list
    dict_list_out = []  # declare empty list for dictionaries list
    while n <= dict_count + 1:
        # add to dict_list list where element is random number fro 0 to 100, key is random lowercase letter,
        # k = max number of items in each dictionary
        dict_list_out.append({ele: randint(0, 101) for ele in random.choices(string.ascii_lowercase, k=randint(1, 5))})
        n += 1
    return dict_list_out


def get_combined_dict(dict_list_in):
    """
    function for creation combined dictionary with following condition:
             if dicts have same key, we will take max value, and rename key with dict number with max value,
             if key is only in one dict - take it as is
    :param dict_list_in: list of dictionaries
    :return: dictionary
    """
    keys_list = []  # declare empty list for all keys of all dictionaries
    for element in dict_list_in:  # for each element in  dict_list
        for key in element.keys():  # for each key of dictionary in dict_list
            keys_list.append(key)  # add this key to keys_list
    # print(keys_list)

    # create empty dictionary which will store list of values from different dictionaries for common keys
    combined_dict = {}
    for key in keys_list:  # for each key in keys_list
        combined_dict[key] = []  # declare empty list for each key in keys_list
        for element in dict_list_in:  # for each list in dict_list
            if key in element.keys():  # if key from keys_list in key of source dictionary
                combined_dict[key].append(element[key])  # add this key and value of the key to combined_dict
            else:
                # add this key and -1 value as indicator to be able find number of dict to combined_dict
                combined_dict[key].append(-1)

    final_dict_out = {}  # declare final dictionary
    i = 0
    for key in combined_dict.keys():  # for ach key in combined_dict
        # create short_values_list and remove all values = -1
        short_values_list = [value for value in combined_dict[key] if value != -1]
        # if len of short_values_list = 1 it means that only one value exists for this key and key should not be renamed
        if len(short_values_list) == 1:
            # add key and value to final dictionary
            final_dict_out[key] = short_values_list[0]
        else:
            # if len of short_values_list != 1 it means that several values exist for this key and key should be renamed
            # and max value should be found
            # find number of dictionary with max value from source dict_list to add to key with _
            key2 = key + '_' + str(combined_dict[key].index(max(combined_dict[key])) + 1)
            # add max value for renamed key to final dictionary
            final_dict_out[key2] = max(combined_dict[key])
            i = i + 1
    return final_dict_out


# part for module 3
def get_sentence_of_last_words(input_text):
    """
    function which return sentence which consists of last word from each sentence in input text
    :param input_text: string
    :return: string
    """
    last_word_sentence_list = []
    for sentence in re.split(r'[.!?]', re.sub(' +', ' ', (input_text.lower().replace('\n', '')))):
        if len(sentence) != 0:
            splitted_words = sentence.strip().split(' ')
            last_word_sentence_list.append(splitted_words[-1])
    output_sentence = ' '.join(last_word_sentence_list).strip().capitalize() + '.'
    return output_sentence


def normalize_case(input_text):
    """
    function which normalizes input text from case point of view
    :param input_text: string
    :return: string
    """
    try:
        input_text_normalized = []
        for paragraph in input_text.lower().splitlines():
            if paragraph.endswith("."):
                paragraph = re.sub('.$', '. ', paragraph)
            sentence_list_normalized = []
            for sentence in paragraph.split('. '):
                sentence = sentence.strip().capitalize()
                sentence_list_normalized.append(sentence)
            paragraph = '. '.join(sentence_list_normalized).strip()
            input_text_normalized.append(paragraph)
        input_text_normalized = '\n'.join(input_text_normalized)
        return input_text_normalized
    except AttributeError:
        print(f'Input string {input_text} is incorrect. normalize_case function cannot be applied.')


def insert_sentence(input_text, n):
    """
    function which inserts sentence consists of last words of each sentence in input text
    into n-th(starts from 0) non-empty paragraph in input text
    :param input_text: string
    :param n: int
    :return: string
    """
    output_text = []
    i = 0
    paragraph_count = 0
    for paragraph in input_text.splitlines():
        if len(paragraph) > 0:
            if paragraph_count == n:
                paragraph = '. '.join(paragraph.split('. '))
                paragraph = (paragraph + ' ' + get_sentence_of_last_words(input_text)).strip()
            paragraph_count += 1
        else:
            paragraph = '. '.join(paragraph.split('. '))
            paragraph = paragraph.strip()
        output_text.append(paragraph)
        i += 1
    output_text = '\n'.join(output_text)
    return output_text


def count_whitespaces(input_text):
    """
    function which counts all whitespaces it input text
    :param input_text: string
    :return: int
    """
    count_whitespaces = 0
    for i in input_text:
        if i in re.findall('\s', input_text):
            count_whitespaces += 1
    return count_whitespaces


# # module 2 implementation
# dict_list = create_dict_list(10)
# print(f'Source list of dictionaries is:')
# print(dict_list)
#
# final_dict = get_combined_dict(dict_list)
# print(f'Final dictionary is:')
# print(final_dict)
#
# print('\n\n')
#
# # module 3 implementation
# source_text = '''homEwork:
#
#   tHis iz your homeWork, copy these Text to variable.
#
#
#
#   You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.
#
#
#
#   it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.
#
#
#
#   last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.'''
#
# last_word_sentence = get_sentence_of_last_words(source_text)
# print(f'Sentence with last words of each existing sentence is:\n{last_word_sentence}\n\n')
#
#
# source_text_normalized = normalize_case(source_text)
# source_text_normalized = insert_sentence(source_text_normalized, 2)
# source_text_normalized = source_text_normalized.replace(' iz ', ' is ')
#
# print(f'Normalized text with inserted sentence and fixed “iz” with correct “is” is:\n{source_text_normalized}')
# print(f'\nNumber of whitespace characters in normalized text is: {count_whitespaces(source_text_normalized)}')
