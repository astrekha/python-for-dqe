import re

source_text = '''homEwork:

  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.'''


# declare empty list for expected words
last_word_sentence_list = []
# replace all '\n' with '' , remove all leading and trailing spaces, convert all words to lowercase,
# remove all extra spaces in source text and split it by sentence end separator ". "
for sentence in re.sub(' +', ' ', source_text.lower().rstrip().replace('\n', '')).split('. '):
    splitted_words = sentence.split(' ')  # split words in each sentence by ' '
    splitted_words = list(filter(None, splitted_words))   # remove empty values from words list
    if len(splitted_words) != 0:
        last_word_sentence_list.append(splitted_words[-1])   # get last word from each sentence
# join expected last words to one sentence and capitalize the sentence
last_word_sentence = ' '.join(last_word_sentence_list).strip().capitalize()
print(f'Sentence with last words of each existing sentence is:\n{last_word_sentence}\n')


source_text_normalized = []    # declare empty list
i = 0   # set counter to find a place where new sentence should be inserted

# split source text to paragraphs by '\n' and convert all words to lowercase
for paragraph in source_text.lower().splitlines():
    # if paragraph ends with dot, replace this dot in the end of paragraph with dot with space
    # to be able to split sentences in paragraph correctly
    if paragraph.endswith("."):
        paragraph = re.sub('.$', '. ', paragraph)
    sentence_list_normalized = []   # declare empty list for sentences
    if i == 6:   # insert new sentence for 6th paragraph
        for sentence in paragraph.split('. '):   # split paragraph by sentences with separator ". "
            sentence = sentence.strip().capitalize()   # remove leading and trailing spaces, capitalize each sentence
            sentence_list_normalized.append(sentence)   # add each sentence to list
            sentence_list_normalized = list(filter(None, sentence_list_normalized))   # remove empty values from list
        # add new sentence consists from last word from each sentence as expected
        sentence_list_normalized.append(last_word_sentence)
    else:
        for sentence in paragraph.split('. '):   # split paragraph by sentences with separator ". "
            sentence = sentence.strip().capitalize()   # remove leading and trailing spaces, capitalize each sentence
            sentence_list_normalized.append(sentence)   # add each sentence to list
    paragraph = '. '.join(sentence_list_normalized).strip()   # join all sentences to paragraph
    source_text_normalized.append(paragraph)   # add paragraph to list of paragraphs
    i += 1   # increase counter
source_text_normalized = '\n'.join(source_text_normalized)   # join paragraphs to text by '\n'


# fix “iz” with correct “is”, but only when it iz a mistake.
source_text_normalized = source_text_normalized.replace(' iz ', ' is ')
print(f'Normalized text with inserted sentence and fixed “iz” with correct “is” is:\n{source_text_normalized}\n')


# calculate number of whitespace characters in this text
count_whitespaces = 0   # set counter = 0
for i in source_text:   # count all spaces, '\n' and '\t' characters
    if i == ' ' or i == '\n' or i == '\t':
        count_whitespaces += 1
print(f'\nNumber of whitespace characters in source text is: {count_whitespaces}')
