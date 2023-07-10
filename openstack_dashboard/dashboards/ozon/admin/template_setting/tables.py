from horizon import tables
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

class UpdateSettingAction(tables.LinkAction):
    name = "update_setting"
    verbose_name = _("Update Setting")
    url = None
    classes = ("ajax-modal",)
    icon = "pencil"
    step = None
    url = "horizon:admin:template_setting:update_setting"

    def get_link_url(self, datum=None):
        return reverse(self.url)


class SettingTable(tables.DataTable):
    name = tables.Column('name', verbose_name=_('Setting Name'))
    value = tables.Column('value', verbose_name=_('Value'))

    def get_object_id(self, obj):
        return obj['name']

    class Meta(object):
        name = "settings"
        verbose_name = _("Settings")
        multi_select = False
        table_actions = (UpdateSettingAction,)

