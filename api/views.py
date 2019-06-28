from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets, mixins, generics, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.settings import api_settings
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404

from vocabulary.models import Word, Chapter, WordProperties, LearningData

from api import serializers


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})


class RegisterUserView(generics.CreateAPIView):
    """Register new user"""
    serializer_class = serializers.UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserViewSet(viewsets.ModelViewSet):
    """Manage users in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.UserDetailSerializer

        return self.serializer_class


class WordViewSet(viewsets.ModelViewSet):
    """Manage words in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Word.objects.all()
    serializer_class = serializers.WordSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        """
        Optionally restricts the returned words to those that start
        with a `startswith` query parameter in the URL
        """
        startswith = self.request.query_params.get('startswith', None)
        if startswith is not None:
            self.queryset = self.queryset.filter(lemma__istartswith=startswith)
        return self.queryset

    def perform_create(self, serializer):
        """Create a new word object"""
        serializer.save(created_by=self.request.user)


class WordPropertiesListView(generics.ListCreateAPIView):
    """Manage word properties in the database"""
    serializer_class = serializers.WordPropertiesSerializer
    queryset = WordProperties.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """Retrieve the word properties for the authenticated user"""
        wordproperties_list = self.queryset.filter(
            chapter__created_by=self.request.user
        )
        serializer = serializers.WordPropertiesSerializer(
            wordproperties_list, many=True
        )
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        write_serializer = serializers.WordPropertiesCreateSerializer(
            data=request.data
        )
        if write_serializer.is_valid():
            wordproperties = write_serializer.save()
            read_serializer = serializers.WordPropertiesSerializer(
                wordproperties
            )
            return Response(
                read_serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WordPropertiesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WordProperties.objects.all()
    serializer_class = serializers.WordPropertiesDetailSerializer


class LearningDataViewSet(viewsets.ModelViewSet):
    """Manage learning data in the database"""
    serializer_class = serializers.LearningDataSerializer
    queryset = LearningData.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


class ChapterListView(generics.ListCreateAPIView):
    queryset = Chapter.objects.all()
    serializer_class = serializers.ChapterSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        if not request.user.username:
            chapters = self.queryset.filter(public=True)
        else:
            chapters = self.queryset.filter(
                Q(created_by=request.user) | Q(public=True)
            )
        serializer = serializers.ChapterSerializer(chapters, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        write_serializer = serializers.ChapterCreateSerializer(
            data=request.data
        )
        if write_serializer.is_valid():
            chapter = write_serializer.save()
            read_serializer = serializers.ChapterDetailSerializer(chapter)
            return Response(
                read_serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChapterDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a chapter"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Chapter.objects.all()
    serializer_class = serializers.ChapterDetailSerializer
