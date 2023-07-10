from django.utils.translation import ugettext_lazy as _

ADD_INSTALLED_APPS = [
    'openstack_dashboard.dashboards.ozon',
]

# The slug of the panel group to be added to HORIZON_CONFIG. Required.
PANEL_GROUP = 'ozon'
# The display name of the PANEL_GROUP. Required.
PANEL_GROUP_NAME = _('Ozon')
# The slug of the dashboard the PANEL_GROUP associated with. Required.
PANEL_GROUP_DASHBOARD = 'admin'
