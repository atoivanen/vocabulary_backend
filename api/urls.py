from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api import views


router = DefaultRouter()
router.register('words', views.WordViewSet)
router.register('wordproperties', views.WordPropertiesViewSet)
router.register('users', views.UserViewSet)
router.register('learningdata', views.LearningDataViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('token/', views.CustomObtainAuthToken.as_view(), name='token'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('chapters/', views.ChapterListView.as_view()),
    path('chapters/<int:pk>', views.ChapterDetailView.as_view()),
]
