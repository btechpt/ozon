from openstack_dashboard.dashboards.ozon.models import TemplateSetting


def context(request):
    template = TemplateSetting.get_data()
    return {
        'logo_url': template['logo'],
        'login_background_url': template['login_background'],
        'primary_color': template['primary_color']
    }