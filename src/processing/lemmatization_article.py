import csv                       
import classla
from common import delete_if_exists, file_to_list


def lemmatize_articles(input_path, output_path):
    """
    Lemmatizatizes textual columns of given articles.

    Args:
        input_path (string):  input path to a csv file
        output_path (string): output path to a csv file
    """
    
    delete_if_exists(output_path)
    
    ID = 0

    print('Lemmatizing ' + str(input_path) + ' in Croatian language.')

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

        # Classla processor
        nlp = classla.Pipeline(lang='hr', processors='lemma, tokenize, pos', use_gpu=False)

        print('Lemmatization started...')

        for row in csv_reader:

            title = row[1]
            subtitle = row[2]
            article_text = row[5]

            # Some articles may have null values
            # which can break loops

            if(len(title) == 0):
                title = 'N/A'

            if(len(subtitle) == 0):
                subtitle = 'N/A'
            
            if(len(article_text) == 0):
                article_text = 'N/A'

            doc_title = nlp(title)
            doc_subtitle = nlp(subtitle)
            doc_article_text = nlp(article_text)

            lem_title =         [word.lemma for sent in doc_title.sentences for word in sent.words]
            lem_subtitle =      [word.lemma for sent in doc_subtitle.sentences for word in sent.words]
            lem_article_text =  [word.lemma for sent in doc_article_text.sentences for word in sent.words]

            lem_title =         (' ').join(lem_title).lower()
            lem_subtitle =      (' ').join(lem_subtitle).lower()
            lem_article_text =  (' ').join(lem_article_text).lower()

            csv_writer.writerow([row[0], lem_title, lem_subtitle, row[3], row[4], lem_article_text, row[6], 
                        row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], 
                        row[16]])
        
    print('Lemmatized file saved at: ' + output_path)


#lemmatize_articles('data/portal_articles_covid_clear.csv', 'data/portal_articles_covid_lemmatized.csv')
lemmatize_articles('data/portal_articles_covid_clear_sentences.csv', 'data/portal_articles_covid_sentences_lemmatized.csv')
