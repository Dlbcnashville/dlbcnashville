from django.db import models
from wagtail.fields import RichTextField
from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, PageChooserPanel
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from authentication.models import User
from django.urls import reverse
from cloudinary.models import CloudinaryField
from django.contrib import messages
# from authentication.models import MembershipStatus
# from wagtailmetadata.models import MetadataPageMixin
# Create your models here.
class CourseIndexPage(Page):
    WAGTAIL_FRONTEND_LOGIN_TEMPLATE = 'authentication/login.html'
    WAGTAIL_FRONTEND_LOGIN_URL = 'authentication:login'
    template = 'courses/all_courses.html'
    intro = RichTextField(blank=True)
    MEMBER_CHOICE= (
        ("Worker", "Worker"),
        ("New Convert", "New Convert"),
        ("Member", "Member"),
    )
    membership_type = models.CharField(max_length=100, choices=MEMBER_CHOICE, default="Member")

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('membership_type'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(CourseIndexPage, self).get_context(request, *args, **kwargs)
        all_workers_courses = CoursePage.objects.live().filter(membership_category__membership_type = 'Worker')
        all_convert_courses = CoursePage.objects.live().filter(membership_category__membership_type = 'New Convert')
        all_member_courses = CoursePage.objects.live().filter(membership_category__membership_type = 'Member')
        all_courses = CoursePage.objects.live()
        completed_courses = CoursePage.objects.live().filter(course_lesson__users = request.user).distinct()
        lessons_empty = []
        for course in self.get_children().live():
            lessons = course.get_children().live()
            for lesson in lessons:
                lessons_empty.append(lesson)

        context["all_workers_courses"] = all_workers_courses
        context["all_convert_courses"] = all_convert_courses
        context["all_member_courses"] = all_member_courses
        context["all_courses"] = all_courses
        context["completed_courses"] = completed_courses
        return context

class CoursePage(Page):
    WAGTAIL_FRONTEND_LOGIN_TEMPLATE = 'authentication/login.html'
    WAGTAIL_FRONTEND_LOGIN_URL = 'authentication:login'
    template = 'courses/course_detail.html'
    course_title = models.CharField(max_length=500, null=True, blank=True)
    course_description = RichTextField(blank=True)
    banner = CloudinaryField("image", null=True, blank=True)
    membership_category = ParentalKey('CourseIndexPage', null=True, blank=True, on_delete=models.SET_NULL, related_name='course_membership')

    content_panels = Page.content_panels + [
        FieldPanel('course_title'),
        FieldPanel('membership_category'),
        FieldPanel('banner'),
        FieldPanel('course_description'),
        
    ]

    def __str__(self):
        return self.course_title
    
    def get_context(self, request, *args, **kwargs):
        context = super(CoursePage, self).get_context(request, *args, **kwargs)
        resources = Resource.objects.filter(course__course_title = self.course_title)
        course_lessons = LessonPage.objects.live().filter(course__course_title = self.course_title)
        member = []
        
        for lesson in course_lessons:
            for user in lesson.users.all():
                if user == request.user:
                    member.append(user)

        if member:
            member_course_completed_lessons = LessonPage.objects.live().filter(course__course_title = self.course_title, course__membership_category__membership_type = request.user.status, users=member[0]).distinct()
            member_course_uncompleted_lessons = LessonPage.objects.live().filter(course__course_title = self.course_title,  course__membership_category__membership_type = request.user.status).exclude(users=member[0]).distinct()
            resume_page = member_course_uncompleted_lessons.first()
            
        else:
            member_course_completed_lessons = []
            member_course_uncompleted_lessons = LessonPage.objects.live().filter(course__course_title = self.course_title,  course__membership_category__membership_type = request.user.status).distinct()
            resume_page = member_course_uncompleted_lessons.first()

        user_lesson = self.get_children()
        completed_lessons = []
        for lesson in member_course_completed_lessons[0:len(user_lesson)]:
            completed_lessons.append(lesson)


        try:
            # code that produces error
            lesson_percent_complete = (len(member_course_completed_lessons)/len(course_lessons))*100
            context["lesson_percent_complete"] = lesson_percent_complete
        except ZeroDivisionError as e:
            messages.error(request,
                           f"No lessons has been added to this course."
                           )

        context["course_lessons"] = course_lessons
        context["member_course_completed_lessons"] = member_course_completed_lessons
        context["member_course_uncompleted_lessons"] = member_course_uncompleted_lessons
        
        context["resume_page"] = resume_page
        context["completed_lessons"] =completed_lessons
        context["resources"] =resources
        # context["message"] = message
        return context
    
class LessonPage(Page):
    WAGTAIL_FRONTEND_LOGIN_TEMPLATE = 'authentication/login.html'
    WAGTAIL_FRONTEND_LOGIN_URL = 'authentication:login'
    template = 'courses/lesson_detail.html'
    lesson_title = models.CharField(max_length=500, null=True, blank=True)
    course =  ParentalKey('CoursePage', null=True, blank=True, on_delete=models.SET_NULL, related_name='course_lesson')
    date_created = models.DateField(auto_now=True)
    lesson_content = RichTextField(blank=True)
    users = ParentalManyToManyField(User, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('lesson_title'),
        FieldPanel('course'),
        FieldPanel('lesson_content'),
        FieldPanel('users'),
    ]

    def __str__(self):
        return self.lesson_title

    def add_authenticated_user(self, user_id):
        try:
            # Fetch the authenticated user
            authenticated_user = User.objects.get(pk=user_id)
            
            if authenticated_user.is_authenticated:
                if authenticated_user in self.users.all():
                    completed = True
                else:
                    completed = False
                    # Add the authenticated user to the many-to-many field
                    self.users.add(authenticated_user)
                    self.save()
                return completed
        except User.DoesNotExist:
            return False
        
    def get_context(self, request, *args, **kwargs):
        context = super(LessonPage, self).get_context(request, *args, **kwargs)
        
        course_lessons = LessonPage.objects.live().filter(course__course_title = self.course.course_title)
        member = []
        
        for lesson in course_lessons:
            for user in lesson.users.all():
                if user == request.user:
                    member.append(user)
        if member:
            member_course_completed_lessons = LessonPage.objects.live().filter(course__course_title = self.course.course_title, users=member[0])
            member_course_uncompleted_lessons = LessonPage.objects.live().filter(course__course_title = self.course.course_title).exclude(users=member[0])
            resume_page = member_course_uncompleted_lessons.first()
            
        else:
            member_course_completed_lessons = []
            member_course_uncompleted_lessons = LessonPage.objects.live().filter(course__course_title = self.course.course_title)
            resume_page = member_course_uncompleted_lessons.first()

        lesson_percent_complete = (len(member_course_completed_lessons)/len(course_lessons))*100
        context["course_lessons"] = course_lessons
        context["member_course_completed_lessons"] = member_course_completed_lessons
        context["member_course_uncompleted_lessons"] = member_course_uncompleted_lessons
        context["lesson_percent_complete"] = lesson_percent_complete
        context["resume_page"] = resume_page
        return context

    def get_next_url(self):
        self.add_authenticated_user(self.owner.id)
        if self.get_next_sibling():
            next = self.get_next_sibling().url
        else:
            next = reverse('course:course_complete')
        return next


@register_snippet
class Resource(models.Model):
    course =  ParentalKey('CoursePage', null=True, blank=True, on_delete=models.SET_NULL, related_name='course_resource')
    resource_title = models.CharField(max_length=500, null=True, blank=True)
    upload_resource = models.URLField(null=True, blank=True, help_text='Add the to the location of the file. E.g. Google Drive')

    panels = [
        FieldPanel('resource_title'),
        FieldPanel('upload_resource'),
        FieldPanel('course'),
    ]
    def __str__(self):
        return self.resource_title

    class Meta:
        verbose_name_plural = "Resources"
    