from django.db import models

from django.urls import reverse # Used in get_absolute_url() to get URL for specified ID

from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel, InlinePanel, FieldRowPanel, MultiFieldPanel, PageChooserPanel
import uuid # Required for unique book instances
from wagtail.models import Page

# Create your models here.
@register_snippet
class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a book genre (e.g. Faith, Prayer etc.)"
    )

    panels = [
        FieldPanel('name'),
    ]

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='genre_name_case_insensitive_unique',
                violation_error_message = "Genre already exists (case insensitive match)"
            ),
        ]

@register_snippet
class LibraryBook(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=500)
    author = models.ForeignKey('BookAuthor', on_delete=models.RESTRICT, null=True)
    # Foreign Key used because book can only have one author, but authors can have multiple books.
    # Author as a string rather than object because it hasn't been declared yet in file.

    isbn = models.CharField('ISBN', max_length=13,
                            unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(
        Genre, help_text="Select a genre for this book")
    
    panels = [
        FieldPanel('title'),
        FieldPanel('author'),
        FieldPanel('isbn'),
        FieldPanel('genre'),
    ]

    def __str__(self):
        """String for representing the Model object."""
        return self.title



class LibraryBookInstance(Page):

    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    book_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book_name = models.ForeignKey('LibraryBook', on_delete=models.RESTRICT, null=True)
    # imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    content_panels = Page.content_panels + [
        FieldPanel('book_id'),
        FieldPanel('book_name'),
        # FieldPanel('imprint'),
        FieldPanel('due_back'),
        FieldPanel('status'),
    ]

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.book_id} ({self.book.title})'

@register_snippet
class BookAuthor(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # date_of_birth = models.DateField(null=True, blank=True)
    # date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'
