from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
class CourseCompleteView(TemplateView):
    template_name = 'courses/lesson_complete.html'
    