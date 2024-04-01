from django.urls import path
from course.views import CourseCompleteView
app_name = "course"

urlpatterns = [
    
    path("course_complete/", CourseCompleteView.as_view(), name="course_complete"),
]