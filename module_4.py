import re

source_text = '''homEwork:

  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.'''


# creation of a function which return sentence which consists of last word from each sentence in input text
def get_sentence_of_last_words(input_text):
    last_word_sentence_list = []
    for sentence in re.split(r'[.!?]', re.sub(' +', ' ', (input_text.lower().replace('\n', '')))):
        if len(sentence) != 0:
            splitted_words = sentence.strip().split(' ')
            last_word_sentence_list.append(splitted_words[-1])
    output_sentence = ' '.join(last_word_sentence_list).strip().capitalize() + '.'
    return output_sentence


# creation of a function which normalizes input text from case point of view
def normalize_case(input_text):
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


# creation of a function which inserts sentence consists of last words of each sentence in input text
# into n-th(starts from 0) non-empty paragraph in input text
def insert_sentence(input_text, n):
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


# creation of a function which counts all whitespaces it input text
def count_whitespaces(input_text):
    count_whitespaces = 0
    for i in input_text:
        if i in re.findall('\s', input_text):
            count_whitespaces += 1
    return count_whitespaces


last_word_sentence = get_sentence_of_last_words(source_text)
print(f'Sentence with last words of each existing sentence is:\n{last_word_sentence}\n\n')


source_text_normalized = normalize_case(source_text)
source_text_normalized = insert_sentence(source_text_normalized, 2)
source_text_normalized = source_text_normalized.replace(' iz ', ' is ')

print(f'Normalized text with inserted sentence and fixed “iz” with correct “is” is:\n{source_text_normalized}')
print(f'\nNumber of whitespace characters in normalized text is: {count_whitespaces(source_text_normalized)}')
