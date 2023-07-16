from typing import Iterable, Optional
from django.db import models

class OzonSettingStore(models.Model):
    id = models.IntegerField(primary_key=True)
    dashboard_name = models.CharField(max_length=256)
    logo = models.ImageField(upload_to='images/')
    login_background = models.ImageField(upload_to='images/')
    primary_color = models.CharField(max_length=256)

    cache = {}

    def save(self, *args, **kwargs):
        OzonSettingStore.cache = {} # Clear memory cache
        return super().save(*args, **kwargs)
    
    @classmethod
    def get_data(cls):
        if cls.cache:
            return cls.cache

        template = OzonSettingStore.objects.first()
        cls.save_cache(template)
        return cls.cache
    
    @classmethod
    def save_cache(cls, result):
        cls.cache = {
            "dashboard_name":  "Ozon Dashboard",
            "logo": "/static/dashboard/img/logo.svg",
            "login_background": "",
            "primary_color": "#0c4869"
        }
    
        if result:
            if result.dashboard_name:
                cls.cache['dashboard_name'] = result.dashboard_name
            if result.dashboard_name:
                cls.cache['logo'] = result.logo.url
            if result.login_background:
                cls.cache['login_background'] = result.login_background.url
            if result.primary_color:
                cls.cache['primary_color'] = result.primary_color
            
