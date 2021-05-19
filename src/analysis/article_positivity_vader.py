import csv                          # Handling csv files
import numpy as np
from common import delete_if_exists, file_to_list
import nltk                         # Natural language manipulation
from nltk.tokenize import word_tokenize               
from nltk.corpus import stopwords
#nltk.download('punkt')
#nltk.download('stopwords')

from google_trans_new import google_translator  
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
import time
import os

import pandas as pd

def sentence_positivity(list_1, analyzer):
    """
    Calculate each sentence positivity using VADER, returns mean
    """
    sentence_weights_list = []

    for sentence in list_1:
        if len(sentence) <= 5:
            continue
        else:
            sentence_weight_dict = analyzer.polarity_scores(sentence)
            sentence_weights_list.append(sentence_weight_dict['compound'])

    total = list(filter(lambda num: num != 0, sentence_weights_list))
    total_mean = np.mean(total)
    #print('Total: ', total)
    #print('Total mean: ', total_mean)
    
    return total_mean
   
    

def article_positivity(input_path, output_path):
    """
    Create 3 columns with a vader positivity rating.

    Args:
        input_path (string): Path to input .csv file.
        output_path (string): Path to output .csv file.
    """
    #delete_if_exists(output_path)

    print('Calculating ' + str(input_path) + ' article positivity (VADER)...')

    analyzer = SentimentIntensityAnalyzer()

    with open(input_path, 'r', encoding = 'utf-8') as csv_read, \
        open(output_path, 'a', encoding = 'utf-8') as csv_write, \
        open(output_path, 'r', encoding = 'utf-8') as csv_read_writer:

        csv_reader = csv.reader(csv_read, delimiter = ',')

        csv_writer = csv.writer(csv_write,
            delimiter=',', 
            quotechar='"', 
            quoting = csv.QUOTE_MINIMAL, 
            lineterminator='\n')
        
        # Add elements to existing list
        csv_reader_writed = csv.reader(csv_read_writer, delimiter = ',')

        headers = ['ID', 'Title', 'Subtitle', 'URL', 
        'Section','Article_text', 'Published_time', 'Modified_time',
        'Author', 'Comments', 'Reaction_love',
        'Reaction_laugh', 'Reaction_hug', 'Reaction_ponder',
        'Reaction_sad', 'Reaction_mad', 'Reaction_mind_blown', 
        'Title_positivity_vader','Subtitle_positivity_vader','Text_positivity_vader', 'Emoji_positivity']
 
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
        
        requests_num = 0

        translate_urls = ['com', 'at', 'ru', 'fr', 'de', 'ch', 'es']
        
        for idx, row in enumerate(csv_reader):

            if idx < num_rows:  
                # Continue if last input
                print('Skipped articles:' + str(idx) + '/' + str(num_rows-1))
                continue
            else:
                title = row[1]
                subtitle = row[2]
                article_text = row[5]

                # Truncate article text because of google translator limit
                if len(article_text) >= 5000:
                    article_text = article_text[:4999]

                try:
                    translator = google_translator(url_suffix = translate_urls)                     
                    title =  translator.translate(title, lang_src='hr', lang_tgt='en')
                    title_positivity_vader = sentence_positivity(title.split('.'), analyzer)
                except:
                    print('Could not translate a title!', ID)
                    title_positivity_vader = 'nan'
                    pass

                try:
                    translator = google_translator(url_suffix = translate_urls)                     
                    subtitle =  translator.translate(subtitle, lang_src='hr', lang_tgt='en')
                    subtitle_positivity_vader = sentence_positivity(subtitle.split('.'), analyzer)
                except:
                    print('Could not translate a subtitle!', ID)
                    article_positivity_vader = 'nan'
                    pass
                
                try:
                    translator = google_translator(url_suffix = translate_urls)                     
                    article_text =  translator.translate(article_text, lang_src='hr', lang_tgt='en')
                    article_positivity_vader = sentence_positivity(article_text.split('.'), analyzer)
                except:
                    print('Could not translate article text!', ID)
                    article_positivity_vader = 'nan'
                    pass
                
                requests_num += 1

                print('Request number/ID: ' + str(requests_num) + '/' + str(ID))
            
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


                csv_writer.writerow([ID, title, subtitle, row[3], row[4], article_text,row[6], 
                            row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], 
                            row[16], title_positivity_vader, subtitle_positivity_vader, article_positivity_vader, reaction_positivity])
                
                ID += 1
        

    print('Clean file saved at: ' + output_path)


article_positivity('data/portal_articles_covid.csv', 
'data/portal_articles_covid_positivity_vader.csv')
