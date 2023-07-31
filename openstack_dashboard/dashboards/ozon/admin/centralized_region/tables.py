from horizon import exceptions, tables
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ngettext_lazy

from openstack_dashboard.dashboards.ozon.models import RegionList

class AddRegionAction(tables.LinkAction):
    name = "add_region"
    verbose_name = _("Add Region")
    url = None
    classes = ("ajax-modal",)
    icon = "pencil"
    step = None
    url = "horizon:admin:centralized_region:add_region"

    def get_link_url(self, datum=None):
        return reverse(self.url)

class EditRegion(tables.LinkAction):
        name = "snapshot"
        verbose_name = _("Edit Region")
        url = "horizon:admin:centralized_region:update_region"
        classes = ("ajax-modal",)
        icon = "pencil"

        def allowed(self, request, instance=None):
            return instance.id != 0
    
        def get_link_url(self, datum=None):
            return reverse(self.url, args=[datum.id])

class DeleteRegion(tables.DeleteAction):

    @staticmethod
    def action_present(count):
        return ngettext_lazy(
            "Delete Region",
            "Delete Regions",
            count
        )

    @staticmethod
    def action_past(count):
        return ngettext_lazy(
            "Deleted Region",
            "Deleted Regions",
            count
        )

    def allowed(self, request, instance=None):
        return instance.id != 0

    def delete(self, request, obj_id):
        try:
            RegionList.objects.filter(id=obj_id).delete()
        except Exception as e:
            exceptions.handle(request, e)

class RegionTable(tables.DataTable):
    url = tables.Column('url', verbose_name=_('URL'))
    name = tables.Column('name', verbose_name=_('Name'))

    # def get_object_id(self, datum):
    #     return datum['id']

    class Meta(object):
        name = "region"
        verbose_name = _("Regions")
        multi_select = False
        table_actions = (AddRegionAction,)
        row_actions = (EditRegion, DeleteRegion)

