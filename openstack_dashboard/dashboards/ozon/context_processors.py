from openstack_dashboard.dashboards.ozon.models import TemplateSetting


def context(request):
    template = TemplateSetting.objects.first()
    if template:
        return {
            'logo_url': template.logo.url,
            'login_background_url': template.login_background.url,
        }
    else:
        return {
            'logo_url': '',
            'login_background_url': '',
        }