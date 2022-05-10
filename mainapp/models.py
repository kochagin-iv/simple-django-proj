from django.db import models

# Create your models here.

from ckeditor.fields import RichTextField
from django.db import models
#from ckeditor.fields import RichTextField
from django.utils.timezone import now
# Create your models here.


class Post(models.Model):
    name = models.CharField(verbose_name='Заголовок', max_length=100)
    short_description = models.TextField(verbose_name='Короткое описание', blank=True)
    description = RichTextField(verbose_name='Описание', blank=True, null=True)
    time_creation = models.DateTimeField(verbose_name='Время создания поста', default=now)

    def save(self):
        super(Post, self).save()

