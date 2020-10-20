from django.contrib import admin

from .models import Tag, Test, Question


admin.site.register(Tag)
admin.site.register(Test)
admin.site.register(Question)
