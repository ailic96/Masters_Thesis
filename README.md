# Diplomski rad

### Student: 
* Anton Ilić
### Mentor:
* _izv. prof. dr. sc._ Ana Meštrović
### Komentor: 
* _doc. dr. sc._ Slobodan Beliga

# Changelog

### __20.04.2021__

#### __src/scraping/article_url_scraper.py__

* Prikupljeni URL-ovi glavnih kategorija u intervalu od 16.04.2021 do 01.01.2020.
* Podaci su spremljeni u:
    * _data/article_urls.txt_

#### __src/scraping/article_scraper.py__

* Prikupljeni svi dostupni metapodaci o svakom pojedinom članku iz _data/article_urls.txt_.
* Većina HTML elemenata s kojih su podaci poscrapani je refaktorirana zbog modifikacije predloška web stranice
od strane samog portala.
* Podaci spremljeni u:
    * _data/portal_articles.csv_

#### __src/analysis/article_quantification.py__

* Ukupna kvantifikacija članaka.
    * __3371__
* Kvantifikacija COVID članaka.
    * __10888__
* Kvantifikacija COVID i Non-COVID članaka po kategorijama.
* Izlazna datoteka
    * _data/portal_articles_covid_binary.csv_

#### __src/processing/article_filter.py__

* U člancima su pretražene riječi vezane uz tematiku koronavirusa, članci koji sadrže te riječi i imaju minimalno 3 emoji reakcije su spremljeni u zasebnu datoteku.
    * __Ukupan broj članaka koji zadovoljava kriterije: 2740__
* Popis COVID-19 riječi: 
    * _word_lists/covid_dictionary.txt_
* Izlazna datoteka: 
    * _data/portal_articles_covid.csv_

#### __src/processing/language_cleaninig.py__

* Iz tekstualnih stupca (naslov, podnaslov, tekst) su otklonjene zaustavne riječi i suvišni znakovi. Rezultati su spremljeni u novu datoteku.
* Popis zaustavnih riječi: 
    * _word_lists/covid_dictionary.txt_
* Izlazna datoteka:
    * _portal_articles_clear.csv_

#### __src/processing/lemmatization_words_list.py__

* Pozitivne i negativne riječi s odgovarajućim težinama su lematizirane modulom Classla
* Riječi prebačene u infinitiv.
* Ulazne datoteke:
    * _word_lists/crosentilex-positives.txt_ , _word_lists/crosentilex-negatives.txt_
* Izlazne datoteke:
    * _word_lists/crosentilex-positives_lemmatized.txt_ , _word_lists/crosentilex-negatives.txt_


#### __src/processing/lemmatization_article.py__

* Svaki tekstualni dio članka (naslov, podnaslov i tekst) su lematizirani modulom Classla i spremljeni u novu datoteku.
* Riječi prebačene u infinitiv.
* Ulazna datoteka:
    * _portal_articles_covid_clear.csv_
* Izlazna datoteka:
    * _portal_articles_covid_lemmatized.csv_

### __src/analysis/article_positivity.py__

* Svakoj riječi iz _data/portal_articles_lemmatized.csv_ je pridodana vrijednost pozitivnosti iz word_lists/crosentilex-(positives/negatives)_lemmatized.txt.
* Posebno je ocijenjena pozitivnost naslova, podnaslova i teksta članka
    * Zbog toga su dodani sljedeći stupci koji predstavljaju pozitivnost svakog pojedinog segmenta:
        * Title_positivity
        * Subtitle_positivity
        * Text_positivity
* Portal ima 7 emoji vrijednosti, a svakoj je pridodan proizvoljni koeficijent pozitivnosti.
* Za svaki članak se koeficijent množi s brojem reakcija korisnika putem tih emoji-a. 
* Rezultat se zbraja i sprema u stupac __Emoji_positivity__
* Ulazna datoteka
    * _data/portal_articles_covid_lemmatized.csv_
* Izlazna datoteka
    * _data/articles_covid_positivity.csv_