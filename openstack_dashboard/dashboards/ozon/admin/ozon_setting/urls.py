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

from django.conf.urls import url
from openstack_auth import utils

from horizon.decorators import require_perms

from . import views

def require_admin(callback):
    return require_perms(callback, tuple(utils.get_admin_permissions()))

urlpatterns = [
    url(r'^$', require_admin(views.IndexView.as_view()), name='index'),
    url(r'^update_setting/$',
        require_admin(views.UpdateSettingView.as_view()), name='update_setting'),
    url(r"^change_region_seamless/$", views.change_region, name='change_region_seamless'),
]

