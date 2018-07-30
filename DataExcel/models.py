from django.db import models


# Create your models here.
class UserInfo(models.Model):
    user = models.CharField(max_length=20, null=False)
    password = models.CharField(max_length=20, null=False)

class ImportRecord(models.Model):
    import_by = models.CharField(max_length=100, null=False)
    #import_date = models.TimeField(auto_now=True)
    import_date = models.DateField(auto_now_add=True)
    import_name = models.CharField(max_length=100, null=False)
    import_year = models.IntegerField()
    import_month = models.IntegerField()
    import_type = models.IntegerField()

class authorityRecord(models.Model):
    authority_by = models.CharField(max_length=100, null=False)
    authority_type = models.IntegerField()
    authority_name = models.CharField(max_length=100, null=False)