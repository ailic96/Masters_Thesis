import os               # For deleting old files 
import csv              # .CSV manipulation
import pandas as pd     # Advanced data manipulation
from common import delete_if_exists, file_to_list


def covid_identifier(input_path, output_path, word_list):
    """
    Filters COVID-19 related articles with more than three emoji reactions.

    Args:
        input_path (string): .csv input file
        output_path (string): .csv output file
        word_list (string): .txt file with COVID related words
    """

    delete_if_exists(output_path)

    csv_input = input_path
    csv_output = output_path
    covid_dict =  file_to_list(word_list)

    article_counter = 0
    covid_counter = 0

    with open(csv_input, 'r', encoding = 'utf-8') as csv_read, \
         open(csv_output, 'a', encoding = 'utf-8') as csv_write:

        csv_reader = csv.reader(csv_read, delimiter = ',')
        csv_writer = csv.writer(csv_write,
            delimiter=',', 
            quotechar='"', 
            quoting = csv.QUOTE_MINIMAL, 
            lineterminator='\n')  
        
        #Add header for new columns
        headers = ['ID', 'Title', 'Subtitle', 'URL', 
        'Section','Article_text', 'Published_time', 'Modified_time',
        'Author', 'Comments', 'Reaction_love',
        'Reaction_laugh', 'Reaction_hug', 'Reaction_ponder',
        'Reaction_sad', 'Reaction_mad', 'Reaction_mind_blown']
        
        # Skip old header, add new a new one
        next(csv_reader, None)
        csv_writer.writerow(headers)

        print('Modifying portal_articles.csv...')
        print('Calculating the number of COVID articles...')

        for row in csv_reader:

            # Rows turned to lower_case
            title= row[1].lower()
            subtitle = row[2].lower()
            article_text = row[5].lower()
            
            reaction_love = int(row[10])
            reaction_laugh = int(row[11])
            reaction_blushy = int(row[12])
            reaction_ponder = int(row[13])
            reaction_sad = int(row[14])
            reaction_mad  = int(row[15])
            reaction_mind_blown = int(row[16])

            # Emoji value total sum used for article filtering
            emoji_sum =  reaction_love + reaction_laugh + reaction_blushy + reaction_ponder + reaction_sad + reaction_mad + reaction_mind_blown


            # Identifies covid articles, based on a list of words
            # in covid_dictionary.txt
            if (any(map(title.__contains__, covid_dict)) 
                or any(map(subtitle.__contains__, covid_dict))
                     or any(map(article_text.__contains__, covid_dict))):

                     if(emoji_sum >= 3):      
                 
                        csv_writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], 
                        row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], 
                        row[16]])
                
                        covid_counter += 1


            article_counter += 1

    print('Total articles:', article_counter)
    print('COVID-19 articles:', covid_counter)


covid_identifier( 'data/portal_articles.csv', 'data/portal_articles_covid.csv', 'word_lists/covid_dictionary.txt')