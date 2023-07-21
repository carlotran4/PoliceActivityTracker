# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Arrestinfo(models.Model):
    cfs_number = models.IntegerField(db_column='CFS_NUMBER', blank=True, null=True)  # Field name made lowercase.
    incident_id = models.TextField(db_column='INCIDENT_ID', blank=True, null=True)  # Field name made lowercase.
    offender_name = models.TextField(db_column='OFFENDER_NAME', blank=True, null=True)  # Field name made lowercase.
    jailed = models.BooleanField(db_column='JAILED', blank=True, null=True)  # Field name made lowercase.
    officer_name = models.TextField(db_column='OFFICER_NAME', blank=True, null=True)  # Field name made lowercase.
    charges = models.TextField(db_column='CHARGES', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'arrestInfo'


class Callinfo(models.Model):
    cfs_number = models.IntegerField(db_column='CFS_NUMBER', blank=True, null=True)  # Field name made lowercase.
    call_datetime = models.DateTimeField(db_column="CALL_DATETIME", auto_now=False, auto_now_add=False)# Field name made lowercase.
    address = models.TextField(db_column='ADDRESS', blank=True, null=True)  # Field name made lowercase.
    appt_number = models.TextField(db_column='APPT_NUMBER', blank=True, null=True)  # Field name made lowercase.
    agency = models.TextField(db_column='AGENCY', blank=True, null=True)  # Field name made lowercase.
    disposition = models.TextField(db_column='DISPOSITION', blank=True, null=True)  # Field name made lowercase.
    calltype = models.TextField(db_column='CALLTYPE', blank=True, null=True)  # Field name made lowercase.
    details = models.TextField(db_column='DETAILS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'callInfo'