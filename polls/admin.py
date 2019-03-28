from django.contrib import admin
from .models import compendium
from .models import coment
from .models import coment_rate
from .models import compendium_rate
from .models import users
from django.contrib.auth.admin import UserAdmin

admin.site.register(users)
admin.site.register(compendium)
admin.site.register(coment)
admin.site.register(coment_rate)
admin.site.register(compendium_rate)


class QuestionAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question_text']

