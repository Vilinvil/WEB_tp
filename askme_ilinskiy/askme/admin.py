from . import models

from django.contrib import admin


# Register your models here.

admin.site.register(models.Tag)
admin.site.register(models.Answer)
admin.site.register(models.Post)
admin.site.register(models.MyUser)
admin.site.register(models.Like2Post)
admin.site.register(models.Like2Answer)
