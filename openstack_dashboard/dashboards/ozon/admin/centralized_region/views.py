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
from django.urls import reverse_lazy, reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions, tables, forms
from openstack_dashboard.dashboards.ozon.models import RegionList
from .forms import RegionForm
from .tables import RegionTable
from django.conf import settings
from types import SimpleNamespace  


class IndexView(tables.DataTableView):
    page_title = _("Setting")
    template_name = "admin/ozon_setting/index.html"
    table_class = RegionTable

    def get_data(self):
        try:
            all_region = RegionList.objects.all()

            regions = [
                SimpleNamespace(**{
                    "id": 0,
                    "url": settings.DEFAULT_REGION[0],
                    "name": settings.DEFAULT_REGION[1],
                })
            ] + [
                SimpleNamespace(**{
                    "id": r.id,
                    "url": r.url,
                    "name": r.name,
                })
                for r in all_region
            ]

            return regions
        except Exception as e:
            exceptions.handle(self.request, _("Unable to retrieve data." + str(e)))
        return []


class UpdateRegionView(forms.ModalFormView):
    form_class = RegionForm
    form_id = "region_form_update"
    modal_id = "update_region_modal"
    modal_header = _("Update Region")
    page_title = _("Update Region")
    submit_label = _("Update Region")
    submit_url = reverse_lazy("horizon:admin:centralized_region:update_region")
    success_url = reverse_lazy("horizon:admin:centralized_region:index")
    template_name = "admin/centralized_region/form_region.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        args = (self.kwargs["id"],)
        context["submit_url"] = reverse("horizon:admin:centralized_region:update_region", args=args)
        return context

    def get_initial(self):
        try:
            region = RegionList.objects.filter(id=self.kwargs["id"]).first()
            if region:
                return {
                    "model_id": region.id,
                    "url": region.url,
                    "name": region.name,
                }

        except Exception:
            exceptions.handle(self.request, _("Unable to retrieve region."))

        return None


class AddRegionView(forms.ModalFormView):
    form_class = RegionForm
    form_id = "region_form_add"
    modal_id = "add_region_modal"
    modal_header = _("Add Region")
    page_title = _("Add Region")
    submit_label = _("Add Region")
    submit_url = reverse_lazy("horizon:admin:centralized_region:add_region")
    success_url = reverse_lazy("horizon:admin:centralized_region:index")
    template_name = "admin/centralized_region/form_region.html"
