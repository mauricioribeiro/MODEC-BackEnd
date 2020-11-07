from django.db import models


class AbstractModel(models.Model):
    """
    Abstract Model for all API concrete models.
    It adds audit metadata
    """
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='Created DateTime')
    updated_on = models.DateTimeField(auto_now=True, verbose_name='Updated DateTime')
    is_active = models.BooleanField(default=True, verbose_name='Active')

    class Meta:
        abstract = True
