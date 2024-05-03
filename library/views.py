from django.shortcuts import render
# Import list view from Django template
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import LibraryBook, BookAuthor, LibraryBookInstance
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
class LibraryBookList(LoginRequiredMixin, ListView):
    model = LibraryBook
    template_name = "library/library3.html"
    paginate_by = 10
    login_url = "authentication:login"
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(LibraryBookList, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        number_of_book_copies = LibraryBookInstance.objects.all().count()
        number_of_books = LibraryBook.objects.all().count()
        onloan_copies =  LibraryBookInstance.objects.filter(status__exact='o').count()
        maintenance_copies = LibraryBookInstance.objects.filter(status__exact='m').count()
        available_copies = LibraryBookInstance.objects.filter(status__exact='a').count()
        context['number_of_book_copies'] = number_of_book_copies
        context['number_of_books'] = number_of_books
        context['available_copies'] = available_copies
        context['onloan_copies'] = onloan_copies
        return context
    
class LibraryBookDetailView(LoginRequiredMixin, DetailView):
    model = LibraryBook
    template_name = "library/library1.html"
    login_url = "authentication:login"
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class BookAuthorList(LoginRequiredMixin, ListView):
    model = BookAuthor
    template_name = "library/author_list.html"
    paginate_by = 10
    login_url = "authentication:login"
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookAuthorList, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        return context
    
class BookAuthorDetailView(LoginRequiredMixin, DetailView):
    model = BookAuthor
    template_name = "library/author_detail.html"
    login_url = "authentication:login"
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author_books = LibraryBook.objects.filter(author=self.object).order_by('-id')
        context['author_books'] = author_books
        return context
    

class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    """Generic class-based view listing books on loan to current user."""
    model = LibraryBookInstance
    template_name = 'library/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    login_url = "authentication:login"
    redirect_field_name = "redirect_to"

    def get_queryset(self):
        return (
            LibraryBookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )
    
class LoanedBooksListView(LoginRequiredMixin, ListView):
    """Generic class-based view listing books on loan to current user."""
    model = LibraryBookInstance
    template_name = 'library/bookinstance_list_borrowed.html'
    paginate_by = 10
    login_url = "authentication:login"
    redirect_field_name = "redirect_to"

    def get_queryset(self):
        return (
            LibraryBookInstance.objects
            .filter(status__exact='o')
            .order_by('due_back')
        )
    
class BookInstanceListView(LoginRequiredMixin, ListView):
    """Generic class-based view listing books on loan to current user."""
    model = LibraryBookInstance
    template_name = 'library/bookinstance_list.html'
    paginate_by = 10
    login_url = "authentication:login"
    redirect_field_name = "redirect_to"

    def get_queryset(self):
        return (
            LibraryBookInstance.objects.all()
        )
