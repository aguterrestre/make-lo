from django.db import models
from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    """
    Clase utilizada para auditoria. Será padre de los models que requieran de
    una auditoria. Será combinada con django-crum.
    """
    user_creation_id = models.ForeignKey(AbstractUser,
                                         on_delete=models.CASCADE,
                                         related_name='user_creation',
                                         null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True,
                                         blank=True)
    user_update_id = models.ForeignKey(AbstractUser,
                                       on_delete=models.CASCADE,
                                       related_name='user_update',
                                       null=True, blank=True)
    date_update = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True  # para que esta clase no se convierta en una tabla bd
