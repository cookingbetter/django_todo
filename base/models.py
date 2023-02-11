from django.db import models
from django.contrib.auth.models import User


# to save model use: Run 'manage.py makemigrations' to make new migrations, and then re-run 'manage.py migrate' to apply them.
# to create admin use: python manage.py createsuperuser

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']     # order it by this value
 