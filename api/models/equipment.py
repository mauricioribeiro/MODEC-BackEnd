from django.core.validators import RegexValidator
from django.db import models

from api.models import Vessel
from api.models.abstract import AbstractModel


class Equipment(AbstractModel):
    """
    Equipment model
    """
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE, verbose_name='Vessel')
    name = models.CharField(null=False, blank=False, max_length=50, verbose_name='Name')
    code = models.CharField(null=False, blank=False, max_length=8, verbose_name='Code', validators=[
        RegexValidator(
            regex=r'^[A-Za-z0-9]*$',
            message='Code must be alphanumeric',
            code='invalid_code'
        )
    ])
    location = models.CharField(null=False, blank=False, max_length=100, verbose_name='Location')

    def __str__(self):
        return f'Equipment {self.code}' if self.code else super().__str__()
