from django.contrib import admin
from .models import Task

admin.site.register(Task)       # now we can see Task model in admin panel
