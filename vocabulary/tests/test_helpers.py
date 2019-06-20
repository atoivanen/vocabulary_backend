from django.test import TestCase
from django.contrib.auth import get_user_model

from vocabulary.helpers import helpers_fr_fi
from vocabulary.models import Word, Chapter, WordProperties
from vocabulary.tests.test_models import create_word, SOURCE, TARGET


class HelperTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'testuser',
            'testpass'
        )

    def test_analyze_text(self):
        class nlp:
            def __init__(self, text, is_alpha, pos_, lemma_):
                self.text = text
                self.is_alpha = is_alpha
                self.pos_ = pos_
                self.lemma_ = lemma_

        t1 = nlp('Il', True, 'PRON', 'il')
        t2 = nlp('fait', True, 'VERB', 'faire')
        t3 = nlp('beau', True, 'ADJ', 'beau')
        t4 = nlp('.', False, 'PUNCT', '.')
        t5 = nlp('belle', True, 'ADJ', 'beau')
        t6 = nlp('beaux', True, 'ADJ', 'beau')

        spacy_doc_mock = [t1, t2, t3, t4, t5, t6]
        dict = helpers_fr_fi.analyze_text(spacy_doc_mock)

        test_dict = {
            'il': {'pos': 'PRON', 'count': 1},
            'faire': {'orig': ['fait'], 'pos': 'VERB', 'count': 1},
            'beau': {'pos': 'ADJ', 'count': 3, 'orig': ['belle', 'beaux']}
        }

        self.assertEqual(test_dict, dict)

    def test_translate_words(self):
        """Test getting translations for words"""
        create_word(
            user=self.user, lemma='petit', translation='pieni', pos='ADJ'
        )
        create_word(
            user=self.user, lemma='table', translation='pöytä', pos='NOUN'
        )
        create_word(
            user=self.user, lemma='dormir', translation='nukkua', pos='VERB'
        )
        dict = {'petit': {'pos': 'ADJ'},
                    'table': {'pos': 'NOUN'},
                    'dormir': {'pos': 'VERB'},
                    'asdf': {'pos': 'X'}
                }
        test_word_list = Word.objects.filter(
            lemma__in=['petit', 'table', 'dormir']
        ).order_by('lemma')
        word_list = helpers_fr_fi.translate_words(
            dict, SOURCE, TARGET
        )
        word_list.sort(key=lambda x: x.lemma)

        self.assertSequenceEqual(test_word_list, word_list)
