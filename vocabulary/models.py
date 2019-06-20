from django.db import models
from django.contrib.auth.models import User

DEFAULT_TITLE = 'Teksti'

class Word(models.Model):
    """Word with its translation and some linguistic properties"""
    # Gender choices
    FEMININE = 'f'
    MASCULINE = 'm'
    NEUTER = 'n'

    # Part-of-speech tags as in spacy.io.annotation
    ADJECTIVE = 'ADJ'
    ADPOSITION = 'ADP'
    ADVERB = 'ADV'
    AUXILIARY = 'AUX'
    CONJUNCTION = 'CONJ'
    CCONJUNCTION = 'CCONJ'
    DETERMINER = 'DET'
    INTERJECTION = 'INTJ'
    NOUN = 'NOUN'
    NUMERAL = 'NUM'
    PARTICLE = 'PART'
    PRONOUN = 'PRON'
    PROPERNOUN = 'PROPN'
    SCONJUNCTION = 'SCONJ'
    SYMBOL = 'SYM'
    VERB = 'VERB'
    OTHER = 'X'
    SPACE = 'SPACE'

    # Language choices
    FRENCH = 'fr'
    FINNISH = 'fi'

    GENDER_CHOICES = (
        (FEMININE, 'Feminine'),
        (MASCULINE, 'Masculine'),
        (NEUTER, 'Neuter'),
    )
    POS_CHOICES = (
        (ADJECTIVE, 'Adjective'),
        (ADPOSITION, 'Adposition'),
        (ADVERB, 'Adverb'),
        (AUXILIARY, 'Auxiliary'),
        (CONJUNCTION, 'Conjunction'),
        (CCONJUNCTION, 'Coordinating conjunction'),
        (DETERMINER, 'Determiner'),
        (INTERJECTION, 'Interjection'),
        (NOUN, 'Noun'),
        (NUMERAL, 'Numeral'),
        (PARTICLE, 'Particle'),
        (PRONOUN, 'Pronoun'),
        (PROPERNOUN, 'Proper noun'),
        (SCONJUNCTION, 'Subordinating conjunction'),
        (SYMBOL, 'Symbol'),
        (VERB, 'Verb'),
        (OTHER, 'Other'),
        (SPACE, 'Space'),
    )
    LANGUAGE_CHOICES = (
        (FRENCH, 'French'),
        (FINNISH, 'Finnish'),
    )
    lemma = models.CharField(max_length=255)
    translation = models.CharField(max_length=255)
    pos = models.CharField(
        max_length=5, choices=POS_CHOICES, verbose_name='Part-of-speech'
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    source_lang = models.CharField(
        max_length=2, choices=LANGUAGE_CHOICES, verbose_name='Source language'
    )
    target_lang = models.CharField(
        max_length=2, choices=LANGUAGE_CHOICES, verbose_name='Target language'
    )
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='word_created_by'
    )
    modified_date = models.DateTimeField(auto_now=True, null=True)
    modified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='word_modified_by'
    )

    class Meta:
        ordering = ['lemma']
        unique_together = ['lemma', 'pos', 'gender']

    def __str__(self):
        return self.lemma + ' (' + self.pos + ') -> ' + self.translation


class Chapter(models.Model):
    """Analyzed text"""
    # Language choices
    FRENCH = 'fr'
    FINNISH = 'fi'

    LANGUAGE_CHOICES = (
        (FRENCH, 'French'),
        (FINNISH, 'Finnish'),
    )

    title = models.CharField(max_length=255, default=DEFAULT_TITLE)
    body = models.TextField()
    public = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chapter_created_by'
        )
    modified_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='chapter_modified_by'
    )
    words = models.ManyToManyField('Word', through='WordProperties')
    source_lang = models.CharField(
        max_length=2, choices=LANGUAGE_CHOICES, verbose_name='Source language'
    )
    target_lang = models.CharField(
        max_length=2, choices=LANGUAGE_CHOICES, verbose_name='Target language'
    )

    class Meta:
        ordering = ['public', 'title']

    def __str__(self):
        return self.title + ': ' + self.body[:50] + '...'

    def summary(self):
        return self.body[:100]


class WordProperties(models.Model):
    """Word information related to chapter"""
    word = models.ForeignKey('Word', on_delete=models.CASCADE)
    token = models.CharField(max_length=255, default='', blank=True)
    frequency = models.IntegerField(default=0)
    chapter = models.ForeignKey('Chapter', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Word Properties'


class LearningData(models.Model):
    """Words that user has practiced"""
    word = models.ForeignKey('Word', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    learned = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Learning Data'
        ordering = ['word']
        unique_together = ['word', 'user']

