from django.core.validators import RegexValidator
from django.db import models
from django.db.models import UniqueConstraint, Q

from api.models.abstract import AbstractModel


class Vessel(AbstractModel):
    """
    Vessel model
    """
    code = models.CharField(null=False, default=None, max_length=5, verbose_name='Code', validators=[
        RegexValidator(
            regex=r'^[A-Za-z]{2}[0-9]{3}$',
            message='Code must be in code format (AA000). Example: \'MV102\'',
            code='invalid_code'
        )
    ])

    class Meta:
        """
        Vessel meta which applies unique constraint for code when vessel is active
        """
        constraints = [
            UniqueConstraint(fields=['code'], condition=Q(status=True), name='unique_vessel_code')
        ]

    def __str__(self):
        return f'Vessel {self.code}' if self.code else super().__str__()
