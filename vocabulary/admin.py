from django.contrib import admin

from .models import Word, Chapter, WordProperties, LearningData

admin.site.register(Word)
admin.site.register(Chapter)
admin.site.register(WordProperties)
admin.site.register(LearningData)
