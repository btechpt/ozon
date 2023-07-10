import base64

from django.core import validators
from django.utils.translation import ugettext_lazy as _

from horizon import forms, messages, exceptions
from openstack_dashboard.dashboards.ozon.models import TemplateSetting


class SettingForm(forms.SelfHandlingForm):
    dashboard_name = forms.CharField(label=_("Dashboard Name"),
                                   required=False)

    logo = forms.ImageField(label=_("Logo"),
                                    required=False)
    login_background = forms.ImageField(label=_("Login Background"),
                            required=False)
    def handle(self, request, data):
        try:
            setting = TemplateSetting.objects.first()
            if setting:
                # Update
                setting.dashboard_name = data['dashboard_name']
                setting.logo = data['logo']
                setting.login_background = data['login_background']

                setting.save()
            else:
                # Create
                setting = TemplateSetting(
                    dashboard_name = data['dashboard_name'],
                    logo = data['logo'],
                    login_background = data['login_background'],
                )
                setting.save()

            messages.success(request, _(f"Successfully updated"))
            return True
        except Exception as e:
            exceptions.handle(request,
                              _('Unable to update.'))
            return False
