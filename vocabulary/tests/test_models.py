from django.test import TestCase
from django.contrib.auth import get_user_model

from vocabulary.models import Word, Chapter, WordProperties


SOURCE = 'fr'
TARGET = 'fi'

def create_word(user, **params):
    """Create a test word"""
    defaults = {
        'lemma': 'mot',
        'translation': 'sana',
        'pos': 'NOUN',
        'source_lang': SOURCE,
        'target_lang': TARGET
    }
    defaults.update(params)
    return Word.objects.create(created_by=user, **defaults)


class ModelTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test',
            password='testpass'
        )
        self.chapter = Chapter.objects.create(
            title='Test',
            body='Il fait beau.',
            created_by=self.user
        )

    def test_word_str(self):
        """Test word string representation"""
        word = create_word(user=self.user)
        self.assertEqual(
            str(word),
                word.lemma + ' (' \
                + word.pos + ') -> ' \
                + word.translation
        )

    def test_word_ordering(self):
        """Test word ordering"""
        self.assertEqual(
            Word._meta.ordering[0],
            'lemma'
        )

    def test_chapter_str(self):
        """Test chapter string representation"""
        self.assertEqual(
            str(self.chapter),
            self.chapter.title + ': ' + self.chapter.body[:50] + '...'
        )

    def test_chapter_summary(self):
        """Test chapter summary representation"""
        self.assertEqual(
            self.chapter.summary(),
            self.chapter.body[:100]
        )

    def test_word_properties_verbose_name_plural(self):
        """Test that WordProperties has correct plural name"""
        self.assertEqual(
            str(WordProperties._meta.verbose_name_plural),
            'Word Properties'
        )
