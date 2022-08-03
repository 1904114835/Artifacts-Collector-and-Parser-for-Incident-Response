# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Iconcache(models.Model):
    idx = models.CharField(primary_key=True, max_length=40)
    mac_addr = models.CharField(db_column='MAC_addr', max_length=40, blank=True, null=True)  # Field name made lowercase.
    path = models.CharField(db_column='Path', max_length=200)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'IconCache'


class BasicInfor(models.Model):
    idx = models.CharField(primary_key=True, max_length=40)
    mac_addr = models.CharField(db_column='MAC_addr', max_length=40, blank=True, null=True)  # Field name made lowercase.
    os_version = models.CharField(db_column='OS_VERSION', max_length=200, blank=True, null=True)  # Field name made lowercase.
    detailed_version = models.CharField(db_column='Detailed_VERSION', max_length=90, blank=True, null=True)  # Field name made lowercase.
    user = models.CharField(db_column='USER', max_length=100, blank=True, null=True)  # Field name made lowercase.
    last_shutdown_time = models.CharField(db_column='Last_ShutDown_Time', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'basic_infor'


class Eventlog(models.Model):
    idx = models.CharField(primary_key=True, max_length=40)
    mac_addr = models.CharField(db_column='MAC_addr', max_length=40, blank=True, null=True)  # Field name made lowercase.
    event_category = models.IntegerField(db_column='Event_Category')  # Field name made lowercase.
    time_generated = models.CharField(db_column='Time_Generated', max_length=25)  # Field name made lowercase.
    source_name = models.CharField(db_column='Source_Name', max_length=100)  # Field name made lowercase.
    event_id = models.IntegerField(db_column='Event_ID', blank=True, null=True)  # Field name made lowercase.
    event_type = models.IntegerField(db_column='Event_Type', blank=True, null=True)  # Field name made lowercase.
    event_data = models.CharField(db_column='Event_Data', max_length=10000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'eventlog'


class RegistryAutorun(models.Model):
    idx = models.CharField(primary_key=True, max_length=40)
    mac_addr = models.CharField(db_column='MAC_addr', max_length=40, blank=True, null=True)  # Field name made lowercase.
    caption = models.CharField(max_length=200, blank=True, null=True)
    command = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'registry_autorun'


class RegistryConnDevice(models.Model):
    idx = models.CharField(primary_key=True, max_length=40)
    mac_addr = models.CharField(db_column='MAC_addr', max_length=40, blank=True, null=True)  # Field name made lowercase.
    connected_devices_name = models.CharField(db_column='Connected_devices_name', max_length=200, blank=True, null=True)  # Field name made lowercase.
    specific_name = models.CharField(max_length=200, blank=True, null=True)
    time = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'registry_conn_device'


class RegistryUsbname(models.Model):
    idx = models.CharField(primary_key=True, max_length=40)
    mac_addr = models.CharField(db_column='MAC_addr', max_length=40, blank=True, null=True)  # Field name made lowercase.
    usb_name = models.CharField(db_column='USB_Name', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'registry_usbname'


class RegistryUserassist(models.Model):
    idx = models.CharField(primary_key=True, max_length=40)
    mac_addr = models.CharField(db_column='MAC_addr', max_length=40, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=200)  # Field name made lowercase.
    session_number = models.CharField(db_column='Session_Number', max_length=10, blank=True, null=True)  # Field name made lowercase.
    run_count = models.CharField(db_column='Run_Count', max_length=10, blank=True, null=True)  # Field name made lowercase.
    last_run_time = models.CharField(db_column='Last_Run_Time', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'registry_userassist'


class RegistryWireless(models.Model):
    idx = models.CharField(primary_key=True, max_length=40)
    mac_addr = models.CharField(db_column='MAC_addr', max_length=40, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=30, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=80, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'registry_wireless'
