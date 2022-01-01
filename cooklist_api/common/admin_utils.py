from django.contrib.admin import ModelAdmin
from django.contrib.postgres import fields
from django.db import models
from django.db.models import JSONField

from django_json_widget.widgets import JSONEditorWidget
from durationwidget.widgets import TimeDurationWidget


class CommonAdminModelMixin:
    formfield_overrides = {
        fields.JSONField: {"widget": JSONEditorWidget},
        JSONField: {"widget": JSONEditorWidget},
        models.DurationField: {"widget": TimeDurationWidget},
    }


class CustomModelAdmin(CommonAdminModelMixin, ModelAdmin):
    pass
