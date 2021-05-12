import csv                          # Handling csv files
import numpy as np
from common import delete_if_exists, file_to_list
import nltk                         # Natural language manipulation
from nltk.tokenize import word_tokenize               
from nltk.corpus import stopwords
#nltk.download('punkt')
#nltk.download('stopwords')

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
import time


def sentence_positivity(list_1, analyzer):
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
    sentence_weights_list = []

    for sentence in list_1:
        time.sleep(1)
        sentence_weight_dict = analyzer.polarity_scores(sentence)
        sentence_weights_list.append(sentence_weight_dict['compound'])

    total = [ elem for elem in sentence_weights_list if sentence_weights_list != 0.0]
    print('Total: ', total)
    total_mean = np.mean(total)
    print('Total mean: ', total_mean)
    
    return total_mean
   
    

def article_positivity(input_path, output_path):
    """
    Create 3 columns with a positivity rating.

    Args:
        input_path (string): Path to input .csv file.
        output_path (string): Path to output .csv file.
    """
    delete_if_exists(output_path)

    ID = 0

    print('Calculating ' + str(input_path) + ' article positivity...')

    analyzer = SentimentIntensityAnalyzer()

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
        'Reaction_sad', 'Reaction_mad', 'Reaction_mind_blown', 
        'Title_positivity_sentence','Subtitle_positivity_sentence','Text_positivity_sentence', 'Emoji_positivity']

        csv_writer.writerow(headers)

        # Skip old header, add new a new one
        next(csv_reader, None)
        #next(csv_reader_positive, None)
        #next(csv_reader_negative, None)

        for row in csv_reader:

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

            #title_positivity_sentence = sentence_positivity(title.split('.'), analyzer)
            subtitle_positivity_sentence = sentence_positivity(subtitle.split('.'), analyzer)
            #article_positivity_sentence = sentence_positivity(article_text.split('.'), analyzer)
            
            title_positivity_sentence = ''
            #subtitle_positivity_sentence =  ''
            article_positivity_sentence = ''
                    


            csv_writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5],row[6], 
                        row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], 
                        row[16], title_positivity_sentence, subtitle_positivity_sentence, article_positivity_sentence, reaction_positivity])
            

    print('Clean file saved at: ' + output_path)


article_positivity('data/portal_articles_covid_clear_sentences.csv', 
'data/portal_articles_covid_positivity_vader.csv')
