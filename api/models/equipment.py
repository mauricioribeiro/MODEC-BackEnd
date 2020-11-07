from country_list import countries_for_language
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import UniqueConstraint, Q

from api.models import Vessel
from api.models.abstract import AbstractModel


class Equipment(AbstractModel):
    """
    Equipment model
    """
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE, verbose_name='Vessel')
    name = models.CharField(null=False, default=None, max_length=50, verbose_name='Name')
    code = models.CharField(null=False, default=None, max_length=8, verbose_name='Code', validators=[
        RegexValidator(
            regex=r'^[A-Za-z0-9]*$',
            message='Code must be alphanumeric',
            code='invalid_code'
        )
    ])
    location = models.CharField(null=False, default=None, max_length=100, verbose_name='Location')

    def __str__(self):
        return f'Equipment {self.code}' if self.code else super().__str__()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Overrode save including checking location
        parent:
        """
        if self.location not in dict(countries_for_language('en')).values():
            raise AttributeError(f'Location "{self.location}" is invalid')

        super().save(force_insert, force_update, using, update_fields)


