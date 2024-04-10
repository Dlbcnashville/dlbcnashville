from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, InlinePanel, PageChooserPanel, FieldRowPanel, MultiFieldPanel
from django.utils.functional import cached_property
from wagtail.fields import RichTextField
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from cloudinary.models import CloudinaryField
# from wagtailmetadata.models import MetadataPageMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your models here.

from datetime import date
from django.core.mail import send_mail
# from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render


class BookIndexPage(Page):
    template = 'books/book_list.html'
    intro = RichTextField(blank=True)
    banner = CloudinaryField("image", null=True, help_text="")

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('banner')
    ]

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        # Get all posts
        books = BookDownload.objects.live().public().order_by('-first_published_at')
        # Paginate all posts by 2 per page
        paginator = Paginator(books, 6)
        # Try to get the ?page=x value
        page = request.GET.get("page")
        try:
            # If the page exists and the ?page=x is an int
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            posts = paginator.page(paginator.num_pages)


        # "posts" will have child pages; you'll need to use .specific in the template
        # in order to access child properties, such as youtube_video_id and subtitle
        context["posts"] = posts
        return context


class FormField(AbstractFormField):
    page = ParentalKey('BookDownload', on_delete=models.CASCADE, related_name='form_fields')


class BookDownload(AbstractEmailForm):
    template = 'books/book.html'
    book_title = models.CharField(max_length=500, blank=True, null=True)
    book_download_link = models.URLField(blank=True, null=True)
    book_cover_image = CloudinaryField('image', null=True, help_text="Upload book cover image")
    thank_you_text = RichTextField(blank=True)
    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('book_title'),
        FieldPanel('book_download_link'),
        FieldPanel("book_cover_image"),

        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

    @cached_property
    def home_page(self):
        return self.get_parent().specific

    def get_context(self, request, *args, **kwargs):
        context = super(BookDownload, self).get_context(request, *args, **kwargs)
        context["home_page"] = self.home_page
        return context

    def get_form_fields(self):
        return self.form_fields.all()

    def serve(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.get_form(request.POST, page=self)
            if form.is_valid():
                self.process_form_submission(form)
                addresses = [x.strip() for x in self.to_address.split(',')]
                # Subject can be adjusted (adding submitted date), be sure to include the form's defined subject field
                submitted_date_str = date.today().strftime('%x')
                subject = f"{self.subject} - {submitted_date_str}"
                # Update the original landing page context with other data
                context = self.get_context(request)

                text_content  = '\n' + '\n' + 'Dear,' + '\t' + str(form.cleaned_data['full_name']) + '\n' + '\n' +'\n'
                download_link = '<a href="{}" style="padding:10px; background:green; margin-top: 20px; color: white;">Download Book</a>'.format(self.report_download_link)
                html_content = render_to_string('books/email_header.html', context, request=request)+text_content+render_to_string('books/registration_email_template.html', context, request=request)+download_link

                msg = EmailMultiAlternatives(subject, text_content, self.from_address, [address for address in addresses]+[form.cleaned_data['email_address']])
                # msg.content_subtype = "html"  # Main content is now text/html
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                landing_page_context = self.get_context(request, *args, **kwargs)
                landing_page_context["home_page"] = self.home_page
                return render(
                    request,
                    self.get_landing_page_template(request),
                    landing_page_context
                )
        else:
            form = self.get_form(page=self)

        context = self.get_context(request)
        context['form'] = form
        context["home_page"] = self.home_page
        return render(
            request,
            self.get_template(request),
            context
        )
    
