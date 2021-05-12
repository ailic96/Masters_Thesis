import os
import requests
import re
import time
import datetime
from bs4 import BeautifulSoup 
from csv import writer
import csv
import json
import cchardet


# Timer start
start = time.time()

# Deletes portal_articles.csv in order to have
# a clean start on every run
if os.path.exists('data/portal_articles.csv'):
    os.remove('data/portal_articles.csv')

if os.path.exists('data/portal_article_logger.txt'):
    os.remove('data/portal_article_logger.txt')


# Opens portal_urls for reading article links
file = open('data/portal_urls.txt', 'r')
# Logs a number of processed URL-s
reporting = open('data/portal_article_logger.txt', 'a')

# Number of lines / URLS to be processed
processed_urls = 1
url_counter = len(open('data/portal_urls.txt').readlines())
print('Found ' + str(url_counter) + ' urls')


# Start time
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
print('Script execution started at: ' + current_time + '\n')

reporting.write('ARTICLE SCRAPER LOG\n')
reporting.write('Found ' + str(url_counter) + ' urls\n')
reporting.write('Script execution started at: ' + current_time + '\n')
reporting.flush()



# Create .csv file and write column headers to it
with open('data/portal_articles.csv', 'a', encoding = 'utf-8') as csv_file:
    csv_writer = writer(csv_file, 
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

    print('Finished creating .csv headers...')

    requests_session = requests.Session()

    print('Processing URL-s...')

    for url in file:

        # If invalid URL detected, proceed to the next one
        try:
            # Returns 403 Forbidden without headers
            response = requests_session.get(url, headers={'User-Agent': 'Mozilla/5.0'})

            # URL Counter
            print('Processed ' + str(processed_urls) + ' / ' + str(url_counter) + ' URL-s')
            #print('Processing URL:\n' + url)

            # BeautifulSoup object initialization
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Initializing variables to prevent missing element errors
            id = int(processed_urls)
            title = ''
            subtitle = ''
            url = ''
            section = ''            #td-ss-main-content
            whole_text = ''
            published_time = ''
            modified_time = ''
            author = ''
            comments = '0'          # Default comment value
            reaction_love = ''      # emoji-11 wpra-reaction
            reaction_laugh = ''     # emoji-4 wpra-reaction
            reaction_blushy = ''    # emoji-36 wpra-reaction
            reaction_ponder = ''    # emoji-40 wpra-reaction
            reaction_sad = ''       # emoji-25 wpra-reaction
            reaction_mad = ''       # emoji-28 wpra-reaction
            reaction_mind_blown = ''# emoji-31 wpra-reaction

            # Title
            title = soup.find(property='og:title').get('content')
            
            # Article subtitle
            # Strip removes extra new lines
            if (soup.find(class_ = 'td-post-sub-title')):
                subtitle = soup.find(class_ = 'td-post-sub-title').get_text().strip()
                subtitle.replace('\n', '\\n')

            #Article URL
            article_url = soup.find(property='og:url').get('content')

            # Due to portal structure change, article category needs to be parsed from class string
            section_raw = soup.find('article').get('class')
            category_raw = section_raw[7]
            section = category_raw[9:].capitalize()

            for tags in soup.find_all('time', class_='entry-date updated td-module-date'):
                if tags.has_attr('datetime'):
                    published_time_raw = tags['datetime']
                    published_time_obj = datetime.datetime.strptime(published_time_raw, '%Y-%m-%dT%H:%M:%S%z')
                    published_time = published_time_obj.date()

            ## Last time article has been modified / Parsing
            #modified_time_raw = soup.find(property='article:modified_time').get('content')
            #modified_time_obj = datetime.datetime.strptime(modified_time_raw, '%Y-%m-%dT%H:%M:%S%z')  
            #modified_time = modified_time_obj.date()

            # Author of article/photo 
            author = soup.find(class_ = 'td-author-name vcard author').get_text()
                
            # Fetching article text
            whole_text = []

            paragraphs = soup.find_all(class_ = 'td-post-content tagdiv-type')

            for paragraph in paragraphs:
                for tekst in paragraph.find_all('p'):
                    # Condition ignores ads and empty <p> elements
                    if (tekst.get_text() == ''):
                        continue
                    # Usef for getting bolded strings
                    elif (tekst.find('strong')):   
                        whole_text.append(tekst.find('strong').get_text().strip('<br>')) 
                        whole_text.append(tekst.get_text())  

                        # Used for getting paragraph header (summary)
                    elif (tekst.find('h2')):
                        whole_text.append(tekst.find('h2').get_text())
                        whole_text.append(tekst.get_text()) 

                    # Used for getting paragraph header (summary)    
                    elif (tekst.find('h3')):
                        whole_text.append(tekst.find('h2').get_text())
                        whole_text.append(tekst.get_text()) 

                    # Used for getting default <p> tag strings
                    else:
                        whole_text.append(tekst.get_text())


            # Turning list into string using join function 
            whole_text = ' '.join(whole_text)

            # Editing string and getting rid of \n 
            whole_text.replace('\n', ' ').replace('\r', '')
            whole_text.replace('\n', '\\n')

            # Comment section
            if (soup.find(class_ = 'td-comments-title block-title')):
                comment = soup.find('h4').get_text()
            
                regex = re.search('(\d*).*', comment)

                if regex:
                    comments = regex.group(1)


            # Find reaction elements
            reaction_love =     soup.find(class_ = re.compile('emoji-11.* wpra-reaction')).get('data-count')
            reaction_laugh =    soup.find(class_ = re.compile('emoji-4.* wpra-reaction')).get('data-count')
            reaction_blushy =   soup.find(class_ = re.compile('emoji-36.* wpra-reaction')).get('data-count')
            reaction_ponder =   soup.find(class_ = re.compile('emoji-40.* wpra-reaction')).get('data-count')
            reaction_sad =      soup.find(class_ = re.compile('emoji-25.* wpra-reaction')).get('data-count')
            reaction_mad =      soup.find(class_ = re.compile('emoji-28.* wpra-reaction')).get('data-count')
            reaction_mind_blown = soup.find(class_ = re.compile('emoji-31.* wpra-reaction')).get('data-count')
            
            # Writes a row into a csv file
            csv_writer.writerow([id, title, subtitle, article_url, 
            section, whole_text, published_time, modified_time,
            author, comments, reaction_love,reaction_laugh,reaction_blushy,
            reaction_ponder, reaction_sad, reaction_mad,
            reaction_mind_blown])
            
            processed_urls += 1
        
        except:
            print('Invalid URL detected: ', url)
            pass


# End execution timer and present results
end = time.time()
print('\nTime spent processing data: ' + str(end - start))

reporting.write('\nTime spent processing data: ' + str(end - start))
reporting.close()