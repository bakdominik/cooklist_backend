from django.db import models

# Create your models here.


class CreateTimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UpdateCreateTimeStampedModel(CreateTimeStampedModel):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
