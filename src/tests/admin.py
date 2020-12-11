from django.contrib import admin

from .models import Tag, Test, Question, SolvedTest, SolvedQuestion


admin.site.register(Tag)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(SolvedTest)
admin.site.register(SolvedQuestion)