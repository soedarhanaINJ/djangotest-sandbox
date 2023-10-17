from django.contrib import admin

from auths import models

admin.site.register(models.User)
admin.site.register(models.UserDesaProfile)

# Register your models here.
