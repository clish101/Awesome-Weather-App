from django.db import models


class City(models.Model):
    name = models.CharField(max_length=50)

    # TODO: Define fields here

    class Meta:
        """Meta definition for City."""

        verbose_name = 'city'
        verbose_name_plural = 'cities'

    def __str__(self):
        """Unicode representation of City."""
        return self.name
