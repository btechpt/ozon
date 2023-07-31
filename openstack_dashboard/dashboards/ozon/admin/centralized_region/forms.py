
from django.utils.translation import ugettext_lazy as _

from horizon import forms, messages, exceptions
from openstack_dashboard.dashboards.ozon.models import RegionList


class RegionForm(forms.SelfHandlingForm):
    url = forms.CharField(label=_("URL"), required=True)
    name = forms.CharField(label=_("Name"), required=True)

    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.model_id = kwargs.get("initial", {}).get("model_id", None)

    def handle(self, request, data):
        try:
            if self.model_id:
                RegionList.objects.filter(id=self.model_id).update(
                    url=data["url"],
                    name=data["name"],
                )
            else:
                RegionList.objects.create(
                    url=data["url"],
                    name=data["name"],
                )

            messages.success(request, _(f"Successfully modify region"))
            return True
        except Exception as e:
            exceptions.handle(request, _("Unable to modify region."))
            return False
