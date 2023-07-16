import base64

from django.core import validators
from django.utils.translation import ugettext_lazy as _

from horizon import forms, messages, exceptions
from openstack_dashboard.dashboards.ozon.models import OzonSettingStore


class SettingForm(forms.SelfHandlingForm):
    dashboard_name = forms.CharField(label=_("Dashboard Name"),
                                   required=False)

    logo = forms.ImageField(label=_("Logo"),
                                    required=False)
    login_background = forms.ImageField(label=_("Login Background"),
                            required=False)
    primary_color = forms.CharField(
        label=_("Primary Color"),
        widget=forms.TextInput(attrs={'type': 'color'})
    )

    def handle(self, request, data):
        try:
            setting = OzonSettingStore.objects.first()
            if setting:
                # Update
                setting.dashboard_name = data['dashboard_name']
                setting.logo = data['logo']
                setting.login_background = data['login_background']
                setting.primary_color = data['primary_color']

                setting.save()
            else:
                # Create
                setting = OzonSettingStore(
                    dashboard_name = data['dashboard_name'],
                    logo = data['logo'],
                    login_background = data['login_background'],
                    primary_color = data['primary_color']
                )
                setting.save()

            messages.success(request, _(f"Successfully updated"))
            return True
        except Exception as e:
            exceptions.handle(request,
                              _('Unable to update.'))
            return False
