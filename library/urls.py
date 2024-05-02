from django.urls import path

app_name = 'library'
# importing views from views..py
from .views import LibraryBookList, LibraryBookDetailView, BookAuthorDetailView, BookAuthorList, LoanedBooksByUserListView, BookInstanceListView
urlpatterns = [
	path(route='books', view=LibraryBookList.as_view(), name='library-books'),
    path(route='book/<int:pk>', view=LibraryBookDetailView.as_view(), name='library-book'),
    path(route='authors', view=BookAuthorList.as_view(), name='library-authors'),
    path(route='author/<int:pk>', view=BookAuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', view=LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('all-book-copies/', view=BookInstanceListView.as_view(), name='all-copies'),
]
