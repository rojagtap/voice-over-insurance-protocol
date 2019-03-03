from django.db import models


class Files(models.Model):
    file_field = models.FileField(upload_to='media/resume', blank=True)
