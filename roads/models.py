from django.db import models


class Roads(models.Model):
    """
    Model class for Roads
    """

    road_code = models.IntegerField(blank=False, null=False, unique=True)
    name = models.TextField(blank=True, null=True)
    length_km = models.TextField(blank=True, null=True)
    geomtype = models.TextField(blank=True, null=True)
    coordinates = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'tbl_roads'


class Azs(models.Model):
    """
    Model class for Azs (Gas station)
    """

    road_code = models.ForeignKey(
        Roads,
        on_delete=models.CASCADE,
        related_query_name="azs",
        db_column='road_code',
        to_field='road_code'
    )
    geomtype = models.TextField(blank=True, null=True)
    coordinates = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'tbl_azs'
