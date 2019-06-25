from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from vocabulary.models import Chapter, WordProperties

from api.serializers import ChapterSerializer, ChapterDetailSerializer, \
                            WordPropertiesSerializer
from api.tests.test_word_api import create_word


CHAPTERS_URL = reverse('api:chapter-list')
WORDPROPERTIES_URL = reverse('api:wordproperties-list')


def detail_url(chapter_id):
    """Return chapter detail URL"""
    return reverse('api:chapter-detail', args=[chapter_id])


def create_chapter(user, public=False, **params):
    """Create and return a test chapter"""
    defaults = {
        'title': 'Chapitre',
        'body': 'Il fait beau.',
        'public': public
    }
    defaults.update(params)

    return Chapter.objects.create(created_by=user, **defaults)


def create_word_properties(word, chapter, **params):
    """Create and return test word properties"""
    defaults = {
        'frequency': 1
    }
    defaults.update(params)

    return WordProperties.objects.create(word=word, chapter=chapter, **defaults)


class PublicChapterApiTests(TestCase):
    """Test unauthenticated chapter API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test',
            'testpass'
        )

    def test_auth_required(self):
        """Test that only public chapters are retrieved"""
        create_chapter(user=self.user)
        create_chapter(user=self.user, public=True)
        res = self.client.get(CHAPTERS_URL)

        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateChapterApiTests(TestCase):
    """Test authenticated chapter API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_chapters(self):
        """Test retrieving a list of chapters"""
        create_chapter(user=self.user)
        create_chapter(user=self.user)

        res = self.client.get(CHAPTERS_URL)

        chapters = Chapter.objects.all().order_by('public', 'title')
        serializer = ChapterSerializer(chapters, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_chapters_limited_to_user(self):
        """Test retrieving chapters for user"""
        user2 = get_user_model().objects.create_user(
            'other',
            'password123'
        )
        create_chapter(user=user2)
        create_chapter(user=self.user)

        res = self.client.get(CHAPTERS_URL)

        chapters = Chapter.objects.filter(created_by=self.user)
        serializer = ChapterSerializer(chapters, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_chapter_detail(self):
        """Test viewing a chapter detail"""
        chapter = create_chapter(user=self.user)
        word1 = create_word(user=self.user, lemma='il')
        word2 = create_word(user=self.user, lemma='faire')
        word3 = create_word(user=self.user, lemma='beau')
        wp1 = create_word_properties(word=word1, chapter=chapter)
        wp2 = create_word_properties(word=word2, chapter=chapter)
        wp3 = create_word_properties(word=word3, chapter=chapter)

        url = detail_url(chapter.id)
        res = self.client.get(url)

        serializer = ChapterDetailSerializer(chapter)
        self.assertEqual(res.data, serializer.data)


class PublicWordPropertiesApiTests(TestCase):
    """Test the publicly available wordproperties API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(WORDPROPERTIES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateWordPropertiesAPITests(TestCase):
    """Test the private wordproperties API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test',
            'testpass'
        )
        self.client.force_authenticate(self.user)

        self.word1 = create_word(user=self.user, lemma='il')
        self.word2 = create_word(user=self.user, lemma='faire')
        self.chapter = create_chapter(user=self.user)

    def test_retrieve_wordproperties_list(self):
        """Test retrieving a list of word properties"""
        create_word_properties(word=self.word1, chapter=self.chapter)
        create_word_properties(word=self.word2, chapter=self.chapter)

        res = self.client.get(WORDPROPERTIES_URL)

        wordproperties = WordProperties.objects.all().order_by('-id')
        serializer = WordPropertiesSerializer(wordproperties, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_wordproperties_limited_to_user(self):
        """Test that word properties for the authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            'other',
            'password123'
        )
        chapter2 = create_chapter(user=user2)
        create_word_properties(word=self.word2, chapter=chapter2)
        wp = create_word_properties(word=self.word1, chapter=self.chapter)

        res = self.client.get(WORDPROPERTIES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['lemma'], wp.word.lemma)
