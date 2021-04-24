import csv                          # Handling csv files
from common import delete_if_exists, file_to_list

import nltk                         # Natural language manipulation
from nltk.tokenize import word_tokenize               
from nltk.corpus import stopwords
#nltk.download('punkt')
#nltk.download('stopwords')


def word_filter_interpunction(text_tokens, stop_words):

    filtered_text = []

    for word in text_tokens:
        if word not in stop_words:
            if word == '?' or word == '!':
                word = '.'
            filtered_text.append(word)
    
    filtered_text = (' ').join(filtered_text).lower()

    return filtered_text


def word_filter_full(text_tokens, stop_words):

    filtered_text = []

    for word in text_tokens:
        if word not in stop_words:
            if word.isalpha():
                filtered_text.append(word)
    
    filtered_text = (' ').join(filtered_text).lower()

    return filtered_text



def clear_stop_words(input_path, output_path, stop_word_input, mode):
    """
    Clears given stopwords from a .csv file.

    Args:
        input_path (string): path to input .csv file
        output_path (string): path to output .csv. file
        stop_word_input (string): path to stopwords .txt file
        mode (int): 0 - full cleaning mode, 1 - interpunction cleaning mode
    """

    delete_if_exists(output_path)

    stop_words = set(file_to_list(stop_word_input))

    ID = 0

    print('Cleaning file ' + str(input_path) + ' of stop words...')

    with open(input_path, 'r', encoding = 'utf-8') as csv_read, \
        open(output_path, 'a', encoding = 'utf-8') as csv_write:

        csv_reader = csv.reader(csv_read, delimiter = ',')
        csv_writer = csv.writer(csv_write,
            delimiter=',', 
            quotechar='"', 
            quoting = csv.QUOTE_MINIMAL, 
            lineterminator='\n')

        headers = ['ID', 'Title', 'Subtitle', 'URL', 
        'Section','Article_text', 'Published_time', 'Modified_time',
        'Author', 'Comments', 'Reaction_love',
        'Reaction_laugh', 'Reaction_hug', 'Reaction_ponder',
        'Reaction_sad', 'Reaction_mad', 'Reaction_mind_blown']

        csv_writer.writerow(headers)

        # Skip old header, add new a new one
        next(csv_reader, None)

        for row in csv_reader:

            title = row[1]
            subtitle = row[2]
            article_text = row[5]

            title = title.lstrip('"')
            subtitle = subtitle.lstrip('"')
                

            title_tokens = word_tokenize(title)
            subtitle_tokens = word_tokenize(subtitle)
            text_tokens = word_tokenize(article_text)

            if mode == 0:
                filtered_title = word_filter_full(title_tokens, stop_words)
                filtered_subtitle = word_filter_full(subtitle_tokens, stop_words)
                filtered_text = word_filter_full(text_tokens, stop_words)
            elif mode == 1:
                filtered_title = word_filter_interpunction(title_tokens, stop_words)
                filtered_subtitle = word_filter_interpunction(subtitle_tokens, stop_words)
                filtered_text = word_filter_interpunction(text_tokens, stop_words)

            ID += 1          

            csv_writer.writerow([ID, filtered_title, filtered_subtitle, row[3], row[4], filtered_text,row[6], 
                        row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], 
                        row[16]])
        

    print('Clean file saved at: ' + output_path)

clear_stop_words('data/portal_articles_covid.csv', 'data/portal_articles_covid_clear.csv', 'word_lists/stop_words.txt', 0)
clear_stop_words('data/portal_articles_covid.csv', 'data/portal_articles_covid_clear_sentences.csv', 'word_lists/interpunction.txt', 1)