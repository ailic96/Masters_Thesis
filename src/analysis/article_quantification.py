import os               # For deleting old files 
import csv              # .CSV manipulation
import pandas as pd     # Advanced data manipulation

from common import delete_if_exists, file_to_list


def covid_identifier(input_path, output_path, covid_wordlist):
    """
    Identifies COVID-19 related articles by searching through
    a dictionary of common expressions used in this kind of articles.

    Args:
        input_path (string): path to input .csv file
        output_path (string): path to output .csv file
        covid_wordlist (string): path to .txt covid_wordlist
    """
    delete_if_exists(output_path)
    covid_dict = file_to_list(covid_wordlist)

    article_counter = 0
    covid_counter = 0
    #print(covid_dict)

    with open(input_path, 'r', encoding = 'utf-8') as csv_read, \
         open(output_path, 'a', encoding = 'utf-8') as csv_write:

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
        'Reaction_sad', 'Reaction_mad', 'Reaction_mind_blown', 'COVID']
        
        # Skip old header, add new a new one
        next(csv_reader, None)
        csv_writer.writerow(headers)

        print('Modifying portal_articles.csv...')
        print('Calculating the number of COVID articles...')

        for row in csv_reader:

            # Rows turned to lower_case
            row[1] = row[1].lower()
            row[2] = row[2].lower()
            row[5] = row[5].lower()

            # Identifies covid articles, based on a list of words
            # in covid_dictionary.txt
            if (any(map(row[1].__contains__, covid_dict)) 
                or any(map(row[2].__contains__, covid_dict))
                     or any(map(row[5].__contains__, covid_dict))):

                #print('found COVID-19 article at id:', row[0])     # Testing
                covid_counter += 1
                row.append(1)
                csv_writer.writerow(row)
            else:
                row.append(0)
                csv_writer.writerow(row)

            # print(row)            
            # Sum of articles
            article_counter += 1

    print('Total articles:', article_counter)
    print('COVID-19 articles:', covid_counter)



def articles_by_category(input_path, output_path):
    """Counts total and COVID related articles by categories. 

    Input:
        CSV File from path
    
    Output:
        CSV File from path
    """

    delete_if_exists(output_path)

    csv_input = input_path
    csv_output = output_path

    # Uses pandas method 'read_csv' for openin a .csv file
    csv_reader = pd.read_csv(csv_input, sep = ',', encoding = 'utf-8')

    # Define a new dataframe using initial dataframe
    dataframe = pd.DataFrame(csv_reader, columns = ['Section', 'COVID'])

    article_category = dataframe.pivot_table(index = ['Section'], 
                                            aggfunc = {'Section':len, 
                                                'COVID':lambda x: (x>0).sum()})
    
    # Correcting column names
    article_category.columns = ['COVID_articles', 'Total_articles']
    article_category.index.name = 'Section'

    # Removing mistakenly added category input, add it to 'Kolumne'
    article_category = article_category.drop('TIHOMIR BRALIĆ')
    article_category.loc[['Kolumne'], ['Total_articles']] += 1

    # Remove irrelevant sub-categories
    article_category = article_category[article_category['Total_articles'] > 51]
    
    article_category.to_csv(csv_output, sep = ',', mode = 'a')

    print('\n************************************************************************')
    print('Articles by category')
    print('************************************************************************')
    print(article_category)


#Function calls

covid_identifier('data/portal_articles.csv', 'data/portal_articles_covid_binary.csv', 'word_lists/covid_dictionary.txt' )
articles_by_category('data/portal_articles_covid_binary.csv', 'tables/portal_articles_category.csv')