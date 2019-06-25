from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from vocabulary.models import Word

from api.serializers import WordSerializer


WORDS_URL = reverse('api:word-list')
SOURCE = 'fr'
TARGET = 'fi'


def create_word(user, **params):
    """Create and return a test word"""
    defaults = {
        'lemma': 'mot',
        'translation': 'sana',
        'pos': 'NOUN',
        'gender': 'm',
        'source_lang': SOURCE,
        'target_lang': TARGET
    }
    defaults.update(params)
    return Word.objects.create(created_by=user, **defaults)


class PublicWordApiTests(TestCase):
    """Test the publicly available word API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test',
            'testpassword'
        )
        self.user2 = get_user_model().objects.create_user(
            'test2',
            'testpassword2'
        )
        self.client = APIClient()

    def test_retrieve_words(self):
        """Test retrieving words"""
        create_word(
            user=self.user, lemma='petit', translation='pieni', pos='ADJ'
        )
        create_word(
            user=self.user, lemma='table', translation='pöytä', pos='NOUN',
            gender='f'
        )
        create_word(
            user=self.user2, lemma='dormir', translation='nukkua', pos='VERB'
        )

        res = self.client.get(WORDS_URL)

        words = Word.objects.all()
        serializer = WordSerializer(words, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)


class PrivateWordApiTests(TestCase):
    """Test the authorized user word API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test',
            'testpassword'
        )
        self.user2 = get_user_model().objects.create_user(
            'test2',
            'testpassword2'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_words(self):
        """Test retrieving words"""
        create_word(
            user=self.user, lemma='petit', translation='pieni', pos='ADJ'
        )
        create_word(
            user=self.user, lemma='table', translation='pöytä', pos='NOUN',
            gender='f'
        )
        create_word(
            user=self.user2, lemma='dormir', translation='nukkua', pos='VERB'
        )

        res = self.client.get(WORDS_URL)

        words = Word.objects.all()
        serializer = WordSerializer(words, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_create_word_successful(self):
        """Test create a new word"""
        payload = {
            'lemma': 'chaise',
            'translation': 'tuoli',
            'pos': 'NOUN',
            'gender': 'f',
            'source_lang': SOURCE,
            'target_lang': TARGET
        }
        self.client.post(WORDS_URL, payload)

        exists = Word.objects.filter(
            lemma=payload['lemma'],
            pos=payload['pos']
        ).exists()
        self.assertTrue(exists)

    def test_create_word_invalid(self):
        """Test creating invalid word fails"""
        payload = {'lemma': ''}
        res = self.client.post(WORDS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
