import csv                          # Handling csv files
import numpy as np
from common import delete_if_exists, file_to_list

import nltk                         # Natural language manipulation
from nltk.tokenize import word_tokenize               
from nltk.corpus import stopwords
#nltk.download('punkt')
#nltk.download('stopwords')

import os
import pandas as pd

def list_contains(list_1, list_positive, list_negative):
    """
    Checks if item from list_1 is in the list_positive or/and in list_negative.
    Calculates article positivity.

    Args:
        list_1 (list): List to compare other two lists with.
        list_positive (list): First list to compare to list_1
        list_negative (list): Second list to compare to list_1

    Returns:
        float: Positvity
    """
    total = 0

    for word in list_1:
        for word_positive in list_positive:
            if(word == word_positive[0]):
                total+=float(word_positive[1])

        for word_negative in list_negative:
            if(word == word_negative[0]):
                total-=float(word_negative[1]) 

    try:
        total_score = total/len(list_1)
    except:
        total_score = 0
        pass

    return total_score



def sentence_positivity(list_1, list_positive, list_negative):
    """
    Checks if item from list_1 is in the list_positive or/and in list_negative.
    Calculates article positivity by each sentence's mean positivity.

    Args:
        list_1 (list): List to compare other two lists with.
        list_positive (list): First list to compare to list_1
        list_negative (list): Second list to compare to list_1

    Returns:
        float: Positvity
    """

    sentence_weights = []

    negative_expressions = ['ne']

    list_1 = list(filter(None, list_1))

    for sentence in list_1:

        sentence_tokens = word_tokenize(sentence)
        sentence_score = 0
        
        # Iterate through each sentence
        for idx, word in enumerate(sentence_tokens):
            
            # If word 'ne' is found, change the whole sentence to 'ne'
            # and decrease positivity by -1 for each occurrence
            if word in negative_expressions:
                sentence_tokens[idx:] = ['ne'] * (len(sentence_tokens) - idx)
                sentence_score -= 1

            # Calculate positivity respectively
            for word_positive in list_positive:
                if(word == word_positive[0]):
                    sentence_score += float(word_positive[1])
                elif word in negative_expressions:      # Skips 'ne'
                    continue

            # Calculate negativity respectively
            for word_negative in list_negative:
                if(word == word_negative[0]):
                    sentence_score -= float(word_negative[1])
                elif word in negative_expressions:      # Skips 'ne'
                    continue
        
        try:
            sentence_score = sentence_score / len(sentence)
        except ZeroDivisionError:
            sentence_score = 0
        finally:
            # Add calculated positivity to a list
            sentence_weights.append(sentence_score)

    total_mean = np.mean(sentence_weights)

    return total_mean


def article_positivity(input_path, output_path, positivity_path, negativity_path):
    """
    Create 3 columns with a positivity rating.

    Args:
        input_path (string): Path to input .csv file.
        output_path (string): Path to output .csv file.
        positivity_path (string): Path to the list of positive expression ratings.
        negativity_path (string): Path to the list of negative expression ratings.
    """
    #delete_if_exists(output_path)

    ID = 0

    print('Calculating ' + str(input_path) + ' article positivity...')

    # Number of lines / URLS to be processed
    processed_articles = 1
    article_counter = len(open('data/portal_articles_covid_sentences_lemmatized.csv', encoding='utf-8').readlines())
    print('Found ' + str(article_counter) + ' articles')


    with open(input_path, 'r', encoding = 'utf-8') as csv_read, \
        open(positivity_path, 'r', encoding = 'utf-8') as csv_read_positive, \
        open(negativity_path, 'r', encoding = 'utf-8') as csv_read_negative, \
        open(output_path, 'a', encoding = 'utf-8') as csv_write:

        csv_reader = csv.reader(csv_read, delimiter = ',')
        csv_reader_positive = list(csv.reader(csv_read_positive, delimiter = ' '))
        csv_reader_negative = list(csv.reader(csv_read_negative, delimiter = ' '))

        csv_writer = csv.writer(csv_write,
            delimiter=',', 
            quotechar='"', 
            quoting = csv.QUOTE_MINIMAL, 
            lineterminator='\n')

        headers = ['ID', 'Title', 'Subtitle', 'URL', 
        'Section','Article_text', 'Published_time', 'Modified_time',
        'Author', 'Comments', 'Reaction_love',
        'Reaction_laugh', 'Reaction_hug', 'Reaction_ponder',
        'Reaction_sad', 'Reaction_mad', 'Reaction_mind_blown', 
        'Title_positivity', 'Subtitle_positivity', 'Text_positivity','Title_positivity_sentence','Subtitle_positivity_sentence','Text_positivity_sentence', 'Emoji_positivity']


        ID = 1

        if os.stat(output_path).st_size > 0:
            df_output = pd.read_csv(output_path, delimiter=',', lineterminator='\n')
            num_rows = len(df_output.index) + 1
        else:
            print('No previous inputs found!')
            num_rows = 0
                

        if num_rows > 0:
            print('File not empty! Number of inputs: ', num_rows + 1)
            print('Continuing...')
            ID = num_rows 
        else:
            csv_writer.writerow(headers)
            # Skip header on iterating
            next(csv_reader, None)

        for idx, row in enumerate(csv_reader):
            
            if idx < num_rows:  
                # Continue if last input
                print('Skipped articles:' + str(idx) + '/' + str(num_rows-1))
                continue
            else:

                print('Processed ' + str(processed_articles) + ' / ' + str(article_counter - num_rows -1) + '(' + str(article_counter-1) +')' + ' articles')

                #print(row)
                title = row[1]
                subtitle = row[2]
                article_text = row[5]

                reaction_love =         float(row[10])     # 1
                reaction_laugh =        float(row[11])     # 0.25
                reaction_hug =          float(row[12])     # 1
                reaction_ponder =       float(row[13])     # -0.25
                reaction_sad =          float(row[14])     # -1
                reaction_mad =          float(row[15])     # -1
                reaction_mind_blown =   float(row[16])     # -0.50

                reaction_count = reaction_love + reaction_laugh + reaction_hug + reaction_ponder + reaction_sad + reaction_mad + reaction_mind_blown
                reaction_positivity = (reaction_love*1 + reaction_laugh*-0.25 + reaction_hug*1 + reaction_ponder*-0.25 + reaction_sad*-1 + reaction_mad*-1 + reaction_mind_blown*-0.5)/reaction_count 
                reaction_positivity = round(reaction_positivity, 2)

                title_positivity    = list_contains(title.split(), csv_reader_positive, csv_reader_negative)
                subtitle_positivity = list_contains(subtitle.split(), csv_reader_positive, csv_reader_negative)
                article_positivity  = list_contains(article_text.split(), csv_reader_positive, csv_reader_negative)

                title_positivity_sentence = sentence_positivity(title.split('.'), csv_reader_positive, csv_reader_negative)
                subtitle_positivity_sentence = sentence_positivity(subtitle.split('.'), csv_reader_positive, csv_reader_negative)
                article_positivity_sentence = sentence_positivity(article_text.split('.'), csv_reader_positive, csv_reader_negative)
                
                csv_writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5],row[6], 
                            row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], 
                            row[16], title_positivity, subtitle_positivity, article_positivity,title_positivity_sentence, 
                            subtitle_positivity_sentence, article_positivity_sentence, reaction_positivity])
                
                processed_articles += 1
                
    print('Clean file saved at: ' + output_path)


article_positivity('data/portal_articles_covid_sentences_lemmatized.csv', 
'data/portal_articles_covid_positivity_extended.csv', 
'word_lists/crosentilex-positives_lemmatized.txt',
'word_lists/crosentilex-negatives_lemmatized.txt')