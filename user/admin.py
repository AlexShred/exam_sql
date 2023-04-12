from django.contrib import admin

from .models import Language, Student, Mentor, Course

admin.site.register(Language)
admin.site.register(Student)
admin.site.register(Mentor)
admin.site.register(Course)
