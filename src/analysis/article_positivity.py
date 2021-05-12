import csv                          # Handling csv files
import numpy as np
from common import delete_if_exists, file_to_list

import nltk                         # Natural language manipulation
from nltk.tokenize import word_tokenize               
from nltk.corpus import stopwords
#nltk.download('punkt')
#nltk.download('stopwords')


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

    return np.round(total/len(list_1), decimals = 5)


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
        
        # Add calculated positivity to a list
        sentence_weights.append(sentence_score/len(list_1))

    #Remove sentence weights if their value equals 0.0
    total = [elem for elem in sentence_weights if elem != 0.0]
    total_mean = np.mean(total)
    
    #print('Sentence weights:\n', sentence_weights)
    #print('Total:\n', total)
    #print('Total mean:\n',total_mean)

    return np.round(total_mean, decimals = 5)



def article_positivity(input_path, output_path, positivity_path, negativity_path):
    """
    Create 3 columns with a positivity rating.

    Args:
        input_path (string): Path to input .csv file.
        output_path (string): Path to output .csv file.
        positivity_path (string): Path to the list of positive expression ratings.
        negativity_path (string): Path to the list of negative expression ratings.
    """
    delete_if_exists(output_path)

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

        csv_writer.writerow(headers)

        # Skip old header, add new a new one
        next(csv_reader, None)
        #next(csv_reader_positive, None)
        #next(csv_reader_negative, None)

        for row in csv_reader:
            
            print('Processed ' + str(processed_articles) + ' / ' + str(article_counter) + ' articles')

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

'''
article_positivity('data/portal_articles_covid_lemmatized.csv', 
'data/portal_articles_covid_positivity.csv', 
'word_lists/crosentilex-positives_lemmatized.txt',
'word_lists/crosentilex-negatives_lemmatized.txt')
'''

article_positivity('data/portal_articles_covid_sentences_lemmatized.csv', 
'data/portal_articles_covid_positivity_extended.csv', 
'word_lists/crosentilex-positives_lemmatized.txt',
'word_lists/crosentilex-negatives_lemmatized.txt')
