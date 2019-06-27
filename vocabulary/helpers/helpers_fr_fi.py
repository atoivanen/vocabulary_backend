from vocabulary.models import Word, Chapter, WordProperties

import sys
import spacy
import fr_core_news_sm

def spacy_analyze(fulltext, source_lang):
    """Use spacy to analyze input text

    Parameters:
    fulltext (string): text
    source_lang (string): language of the input text

    Returns:
    nlp: nlp object

    """
    doc = None

    if (source_lang == 'fr'):
        try:
            nlp = fr_core_news_sm.load(disable=['parser', 'ner'])
            doc = nlp(fulltext)
        except:
            print(sys.exc_info()[0])

    return doc

def analyze_text(spacy_doc):
    """Lemmatize, get word frequencies and part-of-speech tags

    Parameters:
    spacy_doc (spacy nlp object): output from spacy_analyze

    Returns:
    dictionary: {'lemma': {'orig': list, 'pos': string, 'count': int}}
    """
    worddict = {}
    for word in spacy_doc:
        key = word.lemma_.lower()
        # filter out non-alphabetic words
        if word.is_alpha:
            # store word counts and tokens
            if key in worddict:
                orig = worddict[key].get('orig')
                if key == word.text.lower():
                    worddict[key]['count'] += 1
                elif orig:
                    if word.text.lower() not in orig:
                        worddict[key]['orig'].append(word.text.lower())
                        worddict[key]['count'] += 1
                    else:
                        worddict[key]['count'] += 1
                else:
                    worddict[key]['orig'] = [word.text.lower()]
                    worddict[key]['count'] += 1
            elif key == word.text.lower():
                worddict[key] = {'pos': word.pos_, 'count': 1}
            else:
                worddict[key] = {
                    'orig': [word.text.lower()],
                    'pos': word.pos_,
                    'count': 1
                }

    return worddict

def translate_words(worddict, source_lang, target_lang):
    """Find translations of words from database

    Parameters:
    worddict (dictionary): {'lemma': {'pos': string, ...}}
    source_lang (string): source language
    target_lang (string): target language

    Returns:
    list: list of Word objects
    """

    word_list = []

    for key, info in worddict.items():
        try:
            # find translation from database
            word_queryset = Word.objects.filter(
                lemma__iexact=key,
                source_lang=source_lang,
                target_lang=target_lang
            )
            if word_queryset:
                for w in word_queryset:
                    word_list.append(w)
            else:
                print(key)
                # extend the search
                tokens = info.get('orig')
                if tokens:
                    print(tokens)
                    token_queryset = Word.objects.filter(
                        lemma__iexact=tokens[0],
                        source_lang=source_lang,
                        target_lang=target_lang
                    )
                    if token_queryset:
                        for t in token_queryset:
                            word_list.append(t)
        except:
            print(sys.exc_info()[0])
            print ('error when querying database')

    return word_list

def save_chapter(
    body,
    source_lang,
    target_lang,
    title,
    public=False,
    user=None):
    """Save chapter to database

    Parameters:
    body (string): input text
    source_lang (string): source language
    target_lang (string): target language
    title (string): title of the chapter
    public: visible to all users if true
    user (User object): user that created the chapter

    Returns:
    Chapter: Chapter object created from the given parameters

    """
    # save chapter
    chapter = Chapter()
    chapter.body = body
    chapter.created_by = user
    chapter.title = title
    chapter.source_lang = source_lang
    chapter.target_lang = target_lang
    chapter.public = public
    chapter.save()

    fulltext = title + ' ' + body

    doc = spacy_analyze(fulltext, source_lang)
    if doc:
        word_properties = analyze_text(doc)

        word_list = translate_words(
            word_properties,
            source_lang,
            target_lang
        )

        # save word properties related to chapter
        for w in word_list:
            properties = word_properties.get(w.lemma)
            wp = WordProperties()
            if properties:
                if properties['pos'] == w.pos:
                    wp.frequency = properties['count']
                    token_list = properties.get('orig')
                    if token_list:
                        wp.token = ', '.join(token_list)
            wp.chapter = chapter
            wp.word = w
            wp.save()

    return chapter
