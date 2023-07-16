from openstack_auth.backend import KeystoneBackend
from openstack_dashboard.dashboards.ozon.auth import multi_region


class OzonAuthBackend(KeystoneBackend):
    def authenticate(self, request, auth_url=None, **kwargs):
        user = super().authenticate(request, auth_url, **kwargs)
        if user:
            username = kwargs.get('username')
            password = kwargs.get('password')
            if username and password:
                multi_region.save_auth_credentials(request, username, password)
        return user
