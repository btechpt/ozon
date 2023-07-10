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
from openstack_dashboard.dashboards.ozon.models import TemplateSetting
from .forms import SettingForm
from .tables import SettingTable


class IndexView(tables.DataTableView):
    page_title = _("Setting")
    template_name = "admin/template_setting/index.html"
    table_class = SettingTable


    def get_data(self):
        try:
            setting = TemplateSetting.objects.first()
            if not setting:
                return []
                
            return [
                {
                    'name': 'Dashboard Name',
                    'value': setting.dashboard_name
                },
                {
                    'name': 'Logo',
                    'value': format_html('<img src="{}" />', setting.logo.url)
                },
                {
                    'name': 'Login Background',
                    'value': format_html('<img src="{}" />', setting.login_background.url)
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
    submit_url = reverse_lazy("horizon:admin:template_setting:update_setting")
    success_url = reverse_lazy("horizon:admin:template_setting:index")
    template_name = 'admin/template_setting/form_setting.html'


    def get_initial(self):
        try:
            setting = TemplateSetting.objects.first()
            if setting:
                return {
                    'dashboard_name': setting.dashboard_name,
                    'logo': setting.logo,
                    'login_background': setting.login_background,
                }

        except Exception:
            exceptions.handle(self.request,
                              _("Unable to retrieve setting."))

        return None

