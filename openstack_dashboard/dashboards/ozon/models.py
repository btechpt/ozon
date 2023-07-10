from django.db import models

class TemplateSetting(models.Model):
    dashboard_name = models.CharField(max_length=256)
    logo = models.ImageField(upload_to='images/')
    login_background = models.ImageField(upload_to='images/')
