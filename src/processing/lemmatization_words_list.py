import csv                       
import classla
from common import delete_if_exists, file_to_list


def lemmatize_wordlist(input_path, output_path):
    """
    Lemmatization of a given word list

    Args:
        input_path (string): input path to a word list
        output_path (string): output path to a word list
    """
    delete_if_exists(output_path)

    print('Lemmatizing ' + str(input_path) + ' in Croatian language.')

    with open(input_path, 'r', encoding = 'utf-8') as csv_read, \
        open(output_path, 'a', encoding = 'utf-8') as csv_write:

        csv_reader = csv.reader(csv_read, delimiter = ' ')
        csv_writer = csv.writer(csv_write,
            delimiter=' ', 
            quotechar='"', 
            quoting = csv.QUOTE_MINIMAL, 
            lineterminator='\n')

        # Classla processor
        nlp = classla.Pipeline(lang='hr', processors='lemma, tokenize, pos', use_gpu=False)

        print('Lemmatization of ' + input_path + ' started...')

        for row in csv_reader:

            row_word = row[0]
            word_weight = row[1]

            expression = nlp(row_word)

            # Change the word into its lemmatized form
            lem_word = [word.lemma for sent in expression.sentences for word in sent.words]
            lem_word =  ('').join(lem_word)

            csv_writer.writerow([lem_word, word_weight])
        
    print('Lemmatized file saved at: ' + output_path)


lemmatize_wordlist('word_lists/crosentilex-negatives.txt', 'word_lists/crosentilex-negatives_lemmatized.txt')
lemmatize_wordlist('word_lists/crosentilex-positives.txt', 'word_lists/crosentilex-positives_lemmatized.txt')