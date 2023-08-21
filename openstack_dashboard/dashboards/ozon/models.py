import os
from typing import Iterable, Optional
from django.core.exceptions import ValidationError
from django.db import models
from django.core.cache import cache
from openstack_dashboard import settings

class OzonSettingStore(models.Model):
    id = models.IntegerField(primary_key=True)
    dashboard_name = models.CharField(max_length=256)
    logo = models.ImageField(upload_to='images/')
    login_background = models.ImageField(upload_to='images/')
    primary_color = models.CharField(max_length=256)
    fav_icon = models.ImageField(upload_to='images/')


    def save(self, *args, **kwargs):
        cache.delete("ozon_setting")
        return super().save(*args, **kwargs)
    
    @classmethod
    def get_data(cls):
        data = cache.get("ozon_setting")
        if data:
            return data

        template = OzonSettingStore.objects.first()
        cls.save_cache(template)
        return cache.get("ozon_setting")
    
    @classmethod
    def save_cache(cls, result):
        data = {
            "dashboard_name":  "Ozon Dashboard",
            "logo": "/static/dashboard/img/logo.svg",
            "login_background": "",
            "primary_color": "#0c4869",
            "fav_icon": ""
        }
    
        if result:
            if result.dashboard_name:
                data['dashboard_name'] = result.dashboard_name
            if result.dashboard_name:
                data['logo'] = result.logo.url
            if result.login_background:
                data['login_background'] = result.login_background.url
            if result.primary_color:
                data['primary_color'] = result.primary_color
            if result.fav_icon:
                data['fav_icon'] = result.fav_icon.url
            
        cache.set("ozon_setting", data)


class RegionList(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.CharField(max_length=256)
    name = models.CharField(max_length=256)

    @classmethod
    def get_all(cls):
        data = RegionList.objects.all()
        return list(map(lambda d: (d.url, d.name), data))

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)
        settings.AVAILABLE_REGIONS.refresh()
        return result