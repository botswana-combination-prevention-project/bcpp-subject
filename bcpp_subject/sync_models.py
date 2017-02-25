from django.apps import apps as django_apps

from edc_sync.site_sync_models import site_sync_models
from edc_sync.sync_model import SyncModel
from edc_base.model.models.list_model_mixin import ListModelMixin

sync_models = []
app = django_apps.get_app_config('bcpp_subject')
for model in app.get_models():
    if not issubclass(model, ListModelMixin):
        sync_models.append(model._meta.label_lower)

site_sync_models.register(sync_models, SyncModel)
