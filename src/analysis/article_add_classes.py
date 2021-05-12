import pandas as pd
import numpy as np


def assign_classes(path):

    df = pd.read_csv(path, sep=',', encoding='utf-8')

    desc_df = df.describe()
    desc_title_positivity = df['Title_positivity'].describe()
    desc_subtitle_positivity = df['Subtitle_positivity'].describe()
    desc_text_positivity = df['Text_positivity'].describe()

    desc_title_positivity_sentence = df['Title_positivity_sentence'].describe()
    desc_subtitle_positivity_sentence  = df['Subtitle_positivity_sentence'].describe()
    desc_text_positivity_sentence  = df['Text_positivity_sentence'].describe()

    desc_emoji_positivity = df['Emoji_positivity'].describe()

    print('Full stats:\n', desc_df)
    print('Title positivity:\n', desc_title_positivity)
    print('Subtitle positivity:\n', desc_subtitle_positivity)
    print('Article text positivity:\n', desc_text_positivity)
    print('Title positivity (Sentence):\n', desc_title_positivity_sentence)
    print('Subtitle positivity (Sentence):\n', desc_subtitle_positivity_sentence)
    print('Article text positivity (Sentence):\n', desc_text_positivity_sentence)

    print('Emoji positivity:\n', desc_emoji_positivity)

    conditions = [
        (df['Emoji_positivity'] >= 0.1),
        (df['Emoji_positivity'] < 0.1) & (df['Emoji_positivity'] >= 0),
        (df['Emoji_positivity'] < 0)
    ]

    values = ['POSITIVE', 'NEUTRAL', 'NEGATIVE']

    df['Positivity'] = np.select(conditions, values)

    df.to_csv('data/portal_articles_positivity_class.csv', sep=',', encoding='utf-8', index=False)


assign_classes('data/portal_articles_covid_positivity_extended.csv')

