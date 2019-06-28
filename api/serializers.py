from rest_framework import serializers

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from vocabulary.models import Word, Chapter, WordProperties, LearningData
from vocabulary.helpers.helpers_fr_fi import save_chapter


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            request= self.context.get('request'),
            username=username,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class LearningDataForUserSerializer(serializers.ModelSerializer):
    """Serialize learning data for the user detail view"""
    word_id = serializers.ReadOnlyField(source='word.id')
    lemma = serializers.ReadOnlyField(source='word.lemma')
    translation = serializers.ReadOnlyField(source='word.translation')
    pos = serializers.ReadOnlyField(source='word.pos')
    gender = serializers.ReadOnlyField(source='word.gender')
    source_lang = serializers.ReadOnlyField(source='word.source_lang')
    target_lang = serializers.ReadOnlyField(source='word.target_lang')

    class Meta:
        model = LearningData
        fields = (
            'id',
            'word_id',
            'lemma',
            'translation',
            'pos',
            'gender',
            'source_lang',
            'target_lang',
            'learned'
        )


class LearningDataSerializer(serializers.ModelSerializer):
    """Serialize learning data"""
    class Meta:
        model = LearningData
        fields = ('id', 'user', 'word', 'learned')


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user objects"""
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('id',)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserDetailSerializer(UserSerializer):
    """Serialize a user detail"""
    learningdata = LearningDataForUserSerializer(
      source='learningdata_set',
      many=True
    )
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'learningdata'
        )
        read_only_fields = ('id',)


class WordSerializer(serializers.ModelSerializer):
    """Serializer for word objects"""

    class Meta:
        model = Word
        fields = (
            'id',
            'lemma',
            'translation',
            'pos',
            'gender',
            'source_lang',
            'target_lang',
            'created_by',
            'modified_by'
        )
        read_only_fields = ('id',)


class WordPropertiesSerializer(serializers.ModelSerializer):
    """Serialize word properties"""
    word_id = serializers.ReadOnlyField(source='word.id')
    lemma = serializers.ReadOnlyField(source='word.lemma')
    translation = serializers.ReadOnlyField(source='word.translation')
    pos = serializers.ReadOnlyField(source='word.pos')
    gender = serializers.ReadOnlyField(source='word.gender')

    class Meta:
        model = WordProperties
        fields = (
            'id',
            'word_id',
            'lemma',
            'translation',
            'pos',
            'gender',
            'token',
            'frequency'
        )
        read_only_fields = ('id',)


class WordPropertiesCreateSerializer(serializers.ModelSerializer):
    """Serialize word properties creation"""
    class Meta:
        model = WordProperties
        fields = (
            'word',
            'chapter',
            'token',
            'frequency'
        )

    def create(self, validated_data):
        """
        Create and return a new WordProperties instance given the validated data
        """
        return WordProperties.objects.create(**validated_data)


class WordPropertiesDetailSerializer(serializers.ModelSerializer):
    """Serializer for word properties objects"""
    class Meta:
        model = WordProperties
        fields = (
            'id',
            'word',
            'chapter',
            'token',
            'frequency'
        )
        read_only_fields = ('id', 'word', 'chapter')


class ChapterSerializer(serializers.ModelSerializer):
    """Serialize a chapter"""
    class Meta:
        model = Chapter
        fields = (
            'id',
            'title',
            'body',
            'created_date',
            'created_by',
            'modified_date',
            'modified_by',
            'public',
            'source_lang',
            'target_lang'
        )
        read_only_fields = ('id', 'created_date', 'modified_date')


class ChapterCreateSerializer(serializers.ModelSerializer):
    """Serialize chapter creation"""
    class Meta:
        model = Chapter
        fields = (
            'title',
            'body',
            'source_lang',
            'target_lang',
            'created_by',
            'public'
        )

    def create(self, validated_data):
        """Create and return a new Chapter instance given the validated data"""
        title = validated_data.pop('title')
        body = validated_data.pop('body')
        source_lang = validated_data.pop('source_lang')
        target_lang = validated_data.pop('target_lang')
        created_by = validated_data.pop('created_by')
        public = validated_data.pop('public')
        chapter = save_chapter(
            body,
            source_lang,
            target_lang,
            title,
            public,
            created_by
        )
        return chapter


class ChapterDetailSerializer(ChapterSerializer):
    """Serialize a chapter detail"""
    words = WordPropertiesSerializer(
        source='wordproperties_set',
        many=True,
        required=False
    )
    class Meta:
        model = Chapter
        fields = (
            'id',
            'title',
            'body',
            'public',
            'created_date',
            'created_by',
            'modified_date',
            'modified_by',
            'source_lang',
            'target_lang',
            'words'
        )
        read_only_fields = (
            'id',
            'created_date',
            'created_by',
            'modified_date',
            'words'
        )
