# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.forms.models import model_to_dict

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
    ip_addr = models.CharField(db_column='Ip_addr', max_length=100, blank=True, null=True)  # Field name made lowercase.
    os_version = models.CharField(db_column='OS_VERSION', max_length=200, blank=True, null=True)  # Field name made lowercase.
    detailed_version = models.CharField(db_column='Detailed_VERSION', max_length=90, blank=True, null=True)  # Field name made lowercase.
    user = models.CharField(db_column='USER', max_length=100, blank=True, null=True)  # Field name made lowercase.
    last_shutdown_time = models.CharField(db_column='Last_ShutDown_Time', max_length=200, blank=True, null=True)  # Field name made lowercase.
    pc_name = models.CharField(db_column='PC_Name', max_length=40, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=40, blank=True, null=True)  # Field name made lowercase.
    pc_manufa = models.CharField(db_column='PC_manufa', max_length=40, blank=True, null=True)  # Field name made lowercase.
    workgroup = models.CharField(db_column='Workgroup', max_length=40, blank=True, null=True)  # Field name made lowercase.
    model = models.CharField(db_column='Model', max_length=40, blank=True, null=True)  # Field name made lowercase.
    os_name = models.CharField(db_column='OS_name', max_length=40, blank=True, null=True)  # Field name made lowercase.
    os_arch = models.CharField(db_column='OS_arch', max_length=40, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'basic_infor'


class EvtxApplication(models.Model):
    idx = models.CharField(primary_key=True, max_length=40)
    event_category = models.IntegerField(db_column='Event_Category')  # Field name made lowercase.
    time_generated = models.CharField(db_column='Time_Generated', max_length=25)  # Field name made lowercase.
    source_name = models.CharField(db_column='Source_Name', max_length=100)  # Field name made lowercase.
    event_id = models.IntegerField(db_column='Event_ID', blank=True, null=True)  # Field name made lowercase.
    event_type = models.IntegerField(db_column='Event_Type', blank=True, null=True)  # Field name made lowercase.
    event_data = models.CharField(db_column='Event_Data', max_length=10000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'evtx_application'


class EvtxAppxOperational(models.Model):
    idx = models.CharField(primary_key=True, max_length=40)
    event_category = models.IntegerField(db_column='Event_Category')  # Field name made lowercase.
    time_generated = models.CharField(db_column='Time_Generated', max_length=25)  # Field name made lowercase.
    source_name = models.CharField(db_column='Source_Name', max_length=100)  # Field name made lowercase.
    event_id = models.IntegerField(db_column='Event_ID', blank=True, null=True)  # Field name made lowercase.
    event_type = models.IntegerField(db_column='Event_Type', blank=True, null=True)  # Field name made lowercase.
    event_data = models.CharField(db_column='Event_Data', max_length=10000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'evtx_appx_operational'


class EvtxGrouppolicyOperational(models.Model):
    idx = models.CharField(primary_key=True, max_length=40)
    event_category = models.IntegerField(db_column='Event_Category')  # Field name made lowercase.
    time_generated = models.CharField(db_column='Time_Generated', max_length=25)  # Field name made lowercase.
    source_name = models.CharField(db_column='Source_Name', max_length=100)  # Field name made lowercase.
    event_id = models.IntegerField(db_column='Event_ID', blank=True, null=True)  # Field name made lowercase.
    event_type = models.IntegerField(db_column='Event_Type', blank=True, null=True)  # Field name made lowercase.
    event_data = models.CharField(db_column='Event_Data', max_length=10000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'evtx_grouppolicy_operational'


class EvtxNtfsOperational(models.Model):
    idx = models.CharField(primary_key=True, max_length=40)
    event_category = models.IntegerField(db_column='Event_Category')  # Field name made lowercase.
    time_generated = models.CharField(db_column='Time_Generated', max_length=25)  # Field name made lowercase.
    source_name = models.CharField(db_column='Source_Name', max_length=100)  # Field name made lowercase.
    event_id = models.IntegerField(db_column='Event_ID', blank=True, null=True)  # Field name made lowercase.
    event_type = models.IntegerField(db_column='Event_Type', blank=True, null=True)  # Field name made lowercase.
    event_data = models.CharField(db_column='Event_Data', max_length=10000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'evtx_ntfs_operational'


class EvtxPowershellOperational(models.Model):
    idx = models.CharField(primary_key=True, max_length=40)
    event_category = models.IntegerField(db_column='Event_Category')  # Field name made lowercase.
    time_generated = models.CharField(db_column='Time_Generated', max_length=25)  # Field name made lowercase.
    source_name = models.CharField(db_column='Source_Name', max_length=100)  # Field name made lowercase.
    event_id = models.IntegerField(db_column='Event_ID', blank=True, null=True)  # Field name made lowercase.
    event_type = models.IntegerField(db_column='Event_Type', blank=True, null=True)  # Field name made lowercase.
    event_data = models.CharField(db_column='Event_Data', max_length=10000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'evtx_powershell_operational'


class EvtxSecurity(models.Model):
    idx = models.CharField(primary_key=True, max_length=40)
    event_category = models.IntegerField(db_column='Event_Category')  # Field name made lowercase.
    time_generated = models.CharField(db_column='Time_Generated', max_length=25)  # Field name made lowercase.
    source_name = models.CharField(db_column='Source_Name', max_length=100)  # Field name made lowercase.
    event_id = models.IntegerField(db_column='Event_ID', blank=True, null=True)  # Field name made lowercase.
    event_type = models.IntegerField(db_column='Event_Type', blank=True, null=True)  # Field name made lowercase.
    event_data = models.CharField(db_column='Event_Data', max_length=10000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'evtx_security'


class EvtxStoreOperational(models.Model):
    idx = models.CharField(primary_key=True, max_length=40)
    event_category = models.IntegerField(db_column='Event_Category')  # Field name made lowercase.
    time_generated = models.CharField(db_column='Time_Generated', max_length=25)  # Field name made lowercase.
    source_name = models.CharField(db_column='Source_Name', max_length=100)  # Field name made lowercase.
    event_id = models.IntegerField(db_column='Event_ID', blank=True, null=True)  # Field name made lowercase.
    event_type = models.IntegerField(db_column='Event_Type', blank=True, null=True)  # Field name made lowercase.
    event_data = models.CharField(db_column='Event_Data', max_length=10000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'evtx_store_operational'


class EvtxSystem(models.Model):
    idx = models.CharField(primary_key=True, max_length=40)
    event_category = models.IntegerField(db_column='Event_Category')  # Field name made lowercase.
    time_generated = models.CharField(db_column='Time_Generated', max_length=25)  # Field name made lowercase.
    source_name = models.CharField(db_column='Source_Name', max_length=100)  # Field name made lowercase.
    event_id = models.IntegerField(db_column='Event_ID', blank=True, null=True)  # Field name made lowercase.
    event_type = models.IntegerField(db_column='Event_Type', blank=True, null=True)  # Field name made lowercase.
    event_data = models.CharField(db_column='Event_Data', max_length=10000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'evtx_system'


class EvtxWindowsPowershell(models.Model):
    idx = models.CharField(primary_key=True, max_length=40)
    event_category = models.IntegerField(db_column='Event_Category')  # Field name made lowercase.
    time_generated = models.CharField(db_column='Time_Generated', max_length=25)  # Field name made lowercase.
    source_name = models.CharField(db_column='Source_Name', max_length=100)  # Field name made lowercase.
    event_id = models.IntegerField(db_column='Event_ID', blank=True, null=True)  # Field name made lowercase.
    event_type = models.IntegerField(db_column='Event_Type', blank=True, null=True)  # Field name made lowercase.
    event_data = models.CharField(db_column='Event_Data', max_length=10000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'evtx_windows_powershell'


class Jumplist(models.Model):
    idx = models.TextField(blank=True, null=True)
    mac_addr = models.TextField(db_column='MAC_addr', blank=True, null=True)  # Field name made lowercase.
    number_0 = models.TextField(db_column='0', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_1 = models.TextField(db_column='1', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_2 = models.TextField(db_column='2', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_3 = models.TextField(db_column='3', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_4 = models.TextField(db_column='4', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_5 = models.TextField(db_column='5', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_6 = models.TextField(db_column='6', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_7 = models.TextField(db_column='7', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_8 = models.TextField(db_column='8', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_9 = models.TextField(db_column='9', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_10 = models.TextField(db_column='10', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_11 = models.TextField(db_column='11', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_12 = models.TextField(db_column='12', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_13 = models.TextField(db_column='13', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_14 = models.TextField(db_column='14', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_15 = models.TextField(db_column='15', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_16 = models.TextField(db_column='16', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_17 = models.TextField(db_column='17', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_18 = models.TextField(db_column='18', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_19 = models.TextField(db_column='19', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_20 = models.TextField(db_column='20', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_21 = models.TextField(db_column='21', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_22 = models.TextField(db_column='22', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_23 = models.TextField(db_column='23', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_24 = models.TextField(db_column='24', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_25 = models.TextField(db_column='25', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_26 = models.TextField(db_column='26', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_27 = models.TextField(db_column='27', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.

    class Meta:
        managed = False
        db_table = 'jumplist'


class Lnk(models.Model):
    idx = models.TextField(blank=True, null=True)
    mac_addr = models.TextField(db_column='MAC_addr', blank=True, null=True)  # Field name made lowercase.
    number_0 = models.TextField(db_column='0', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_1 = models.TextField(db_column='1', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_2 = models.TextField(db_column='2', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_3 = models.TextField(db_column='3', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_4 = models.TextField(db_column='4', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_5 = models.TextField(db_column='5', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_6 = models.TextField(db_column='6', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_7 = models.TextField(db_column='7', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_8 = models.TextField(db_column='8', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_9 = models.TextField(db_column='9', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_10 = models.TextField(db_column='10', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_11 = models.TextField(db_column='11', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_12 = models.TextField(db_column='12', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_13 = models.TextField(db_column='13', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_14 = models.TextField(db_column='14', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_15 = models.TextField(db_column='15', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_16 = models.TextField(db_column='16', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_17 = models.TextField(db_column='17', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_18 = models.TextField(db_column='18', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_19 = models.TextField(db_column='19', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_20 = models.TextField(db_column='20', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_21 = models.TextField(db_column='21', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_22 = models.TextField(db_column='22', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_23 = models.TextField(db_column='23', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_24 = models.TextField(db_column='24', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_25 = models.TextField(db_column='25', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_26 = models.TextField(db_column='26', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_27 = models.TextField(db_column='27', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.

    class Meta:
        managed = False
        db_table = 'lnk'


class Prefetch(models.Model):
    idx = models.CharField(primary_key=True, max_length=40)
    mac_addr = models.CharField(db_column='MAC_addr', max_length=40, blank=True, null=True)  # Field name made lowercase.
    pf_name = models.CharField(db_column='Pf_name', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    exe_name = models.CharField(db_column='EXE_name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    run_count = models.CharField(db_column='Run_count', max_length=10, blank=True, null=True)  # Field name made lowercase.
    last_run = models.CharField(max_length=500, blank=True, null=True)
    vol_0_name = models.CharField(db_column='Vol_0_name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    vol_0_create_t = models.CharField(db_column='Vol_0_create_T', max_length=50, blank=True, null=True)  # Field name made lowercase.
    vol_0_sn = models.CharField(db_column='Vol_0_SN', max_length=40, blank=True, null=True)  # Field name made lowercase.
    vol_1_name = models.CharField(db_column='Vol_1_name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    vol_1_create_t = models.CharField(db_column='Vol_1_create_T', max_length=50, blank=True, null=True)  # Field name made lowercase.
    vol_1_sn = models.CharField(db_column='Vol_1_SN', max_length=40, blank=True, null=True)  # Field name made lowercase.
    directory_strings = models.TextField(db_column='Directory_Strings', blank=True, null=True)  # Field name made lowercase.
    resources = models.TextField(db_column='Resources', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'prefetch'


class RecycleBin(models.Model):
    idx = models.CharField(max_length=40)
    mac_addr = models.CharField(db_column='MAC_addr', max_length=40, blank=True, null=True)  # Field name made lowercase.
    deleted_date = models.CharField(max_length=40, blank=True, null=True)
    file_type = models.CharField(max_length=20, blank=True, null=True)
    file_size = models.CharField(max_length=20, blank=True, null=True)
    file_path = models.CharField(max_length=200, blank=True, null=True)
    file_name = models.CharField(max_length=100, blank=True, null=True)
    ifile_name = models.CharField(max_length=200, blank=True, null=True)
    rfile_name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recycle_bin'


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


class Win10Activity(models.Model):
    idx = models.TextField(blank=True, null=True)
    mac_addr = models.TextField(db_column='MAC_addr', blank=True, null=True)  # Field name made lowercase.
    last_modification_time = models.TextField(db_column='Last Modification Time', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    expiration_time = models.TextField(db_column='Expiration Time', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    last_modification_time_on_client = models.TextField(db_column='Last Modification Time on Client', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    start_time = models.TextField(db_column='Start Time', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    time_created_in_cloud = models.TextField(db_column='Time Created in Cloud', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    etag = models.BigIntegerField(db_column='ETag', blank=True, null=True)  # Field name made lowercase.
    application = models.TextField(db_column='Application', blank=True, null=True)  # Field name made lowercase.
    display_name = models.TextField(db_column='Display Name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    display_text = models.TextField(db_column='Display Text', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    activity_type = models.TextField(db_column='Activity Type', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    activity_status = models.TextField(db_column='Activity Status', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    priority = models.BigIntegerField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.
    is_local_only = models.TextField(db_column='Is Local Only', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    tag = models.TextField(db_column='Tag', blank=True, null=True)  # Field name made lowercase.
    group = models.TextField(db_column='Group', blank=True, null=True)  # Field name made lowercase.
    match_id = models.TextField(db_column='Match ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    platform = models.TextField(db_column='Platform', blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    content_uri = models.TextField(db_column='Content Uri', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    app_activity_id = models.TextField(db_column='App Activity ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parent_activity_id = models.TextField(db_column='Parent Activity ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    platform_device_id = models.TextField(db_column='Platform Device ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dds_device_id = models.TextField(db_column='Dds Device ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    clipboard_data_id = models.TextField(db_column='Clipboard Data ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    clipboard_data = models.TextField(db_column='Clipboard Data', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gdpr_type = models.TextField(db_column='GDPR Type', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    package_id_hash = models.TextField(db_column='Package ID Hash', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    original_payload = models.TextField(db_column='Original Payload', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'win10_activity'


class Win10Packageid(models.Model):
    mac_addr = models.TextField(db_column='MAC_addr', blank=True, null=True)  # Field name made lowercase.
    idx = models.TextField(blank=True, null=True)
    activity_id = models.TextField(db_column='Activity ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    platform = models.TextField(db_column='Platform', blank=True, null=True)  # Field name made lowercase.
    package_name = models.TextField(db_column='Package Name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    expiration_time = models.TextField(db_column='Expiration Time', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'win10_packageid'
