# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from html import escape
from django import shortcuts
from django.urls import reverse_lazy
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from horizon import views, exceptions, messages, tables, forms
from openstack_dashboard.dashboards.ozon.models import OzonSettingStore
from .forms import SettingForm
from .tables import SettingTable
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from openstack_auth.views import login
from openstack_dashboard.dashboards.ozon.auth import multi_region




class IndexView(tables.DataTableView):
    page_title = _("Setting")
    template_name = "admin/ozon_setting/index.html"
    table_class = SettingTable


    def get_data(self):
        try:
            setting = OzonSettingStore.objects.first()
            if not setting:
                return []
                
            return [
                {
                    'name': 'Dashboard Name',
                    'value': setting.dashboard_name
                },
                {
                    'name': 'Logo',
                    'value': format_html('<img src="{}" width="100px" />', setting.logo.url)
                },
                {
                    'name': 'Login Background',
                    'value': format_html('<img src="{}" width="100px" />', setting.login_background.url)
                },
                {
                    'name': 'Primary Color',
                    'value': format_html('<div style="width: 300px; height: 50px; background-color: {};"></div>', setting.primary_color)
                },
            ]
        except Exception as e:
            exceptions.handle(self.request,
                              _("Unable to retrieve data." + str(e)))
        return []


class UpdateSettingView(forms.ModalFormView):
    form_class = SettingForm
    form_id = "setting_form_update"
    modal_id = "update_setting_modal"
    modal_header = _("Update Setting")
    page_title = _("Setting")
    submit_label = _("Update Setting")
    submit_url = reverse_lazy("horizon:admin:ozon_setting:update_setting")
    success_url = reverse_lazy("horizon:admin:ozon_setting:index")
    template_name = 'admin/ozon_setting/form_setting.html'


    def get_initial(self):
        try:
            setting = OzonSettingStore.objects.first()
            if setting:
                return {
                    'dashboard_name': setting.dashboard_name,
                    'logo': setting.logo,
                    'login_background': setting.login_background,
                    'primary_color': setting.primary_color,
                }

        except Exception:
            exceptions.handle(self.request,
                              _("Unable to retrieve setting."))

        return None


@csrf_protect
@never_cache
def change_region(request):
    new_post = request.POST.copy()
    cred = multi_region.get_auth_credentials(request)
    new_post['username'] = cred['username']
    new_post['password'] = cred['password']

    if settings.OPENSTACK_KEYSTONE_MULTIDOMAIN_SUPPORT:
        last_domain = request.COOKIES.get('login_domain', None)
        new_post['domain'] = last_domain

    request.POST = new_post
    return login(request)
