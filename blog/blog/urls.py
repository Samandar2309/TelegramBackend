from django.urls import path
from .views import BookList, BookDetail

urlpatterns = [
    path('book/', BookList.as_view(), name='book-list'),
    path('book/<int:pk>/', BookDetail.as_view(), name='book-detail'),
]
