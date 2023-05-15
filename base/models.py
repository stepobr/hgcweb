from django.db import models
from django.utils import timezone
import threading
# ---------- Base section

class OraclePkCache:

    class OraclePkCacheItem:

        def __init__(self):
            self.lock = threading.Lock()
            self.size = 0
            self.curr = 0

    def __init__(self, cache_size = 20, db_name = 'core'):
        self.cache_size = cache_size
        self.db_name = db_name
        self.lock = threading.Lock()
        self.cache = {}

    def get(self, seq_name):

        # Adding new entry to cache if does not exist
        if seq_name not in self.cache:
            with self.lock:
                if seq_name not in self.cache:
                    self.cache[seq_name] = self.OraclePkCacheItem()

        item = self.cache[seq_name]

        # Get next PK if available, or reset from sequence
        with item.lock:

            # Reset PK cache
            if item.size == 0:
                c = connections[self.db_name].cursor()
                c.execute("SELECT %s.nextval FROM dual" % seq_name)
                item.curr = c.fetchall()[0][0]
                item.size = self.cache_size
                c.close()
            
            # Get next item
            id = item.curr
            item.curr = item.curr + 1
            item.size = item.size - 1
            return id

class Base(): 
    is_record_deleted = models.CharField(max_length=1, default='F', null=False)
    record_insertion_time = models.DateTimeField(null=False, default=timezone.now)
    record_insertion_user = models.TextField(max_length=50, null=False)
    record_lastupdate_time = models.DateTimeField()
    record_lastupdate_user = models.TextField(max_length=50)
    comment_description = models.TextField(max_length=4000)

    class Meta: 
        proxy = False
        # app_label = 'construct'


class ModelBase(models.Model):

    class Meta:
        abstract = True

    def save(self):
        ModelBase.populate_pk(self)
        super().save()

    pk_cache = OraclePkCache(20, 'construct-dev')

    @staticmethod
    def populate_pk(obj):
        if obj.pk == None and hasattr(obj, 'PK_SEQUENCE_NAME'):
            obj.pk = ModelBase.pk_cache.get(obj.PK_SEQUENCE_NAME)

# ---------- Management

class Institution(ModelBase, Base):

    # class _InstitutionManager(models.Manager):

    #     def order(self, field, order):
    #         option = ''
    #         if (order == 'desc'):
    #             option = '-'
    #         return super().get_queryset().order_by(option + field)
    
    # objects = models.Manager()
    # institutions = _InstitutionManager()

    institution_id = models.AutoField(primary_key=True)
    institute_code = models.IntegerField()
    name = models.TextField(max_length=256)
    town = models.TextField(max_length=128)
    country = models.TextField(max_length=3)
    is_record_deleted = models.CharField(max_length=1, default='F', null=False)
    record_insertion_time = models.DateTimeField(null=False, default=timezone.now)
    record_insertion_user = models.TextField(max_length=50, null=False)
    record_lastupdate_time = models.DateTimeField()
    record_lastupdate_user = models.TextField(max_length=50)
    comment_description = models.TextField(max_length=4000)
    # class Meta:
    #     db_table = '"CMS_HGC_CORE_MANAGEMNT"."INSTITUTIONS"'
    
    def __str__(self):
        return str(self.name)

class Location(models.Model):

    location_id = models.AutoField(primary_key=True)
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE, null=False)
    location_name = models.TextField(max_length=40, null=False)
    is_record_deleted = models.CharField(max_length=1, default='F', null=False)
    record_insertion_time = models.DateTimeField(null=False, default=timezone.now)
    record_insertion_user = models.TextField(max_length=50, null=False)
    record_lastupdate_time = models.DateTimeField()
    record_lastupdate_user = models.TextField(max_length=50)
    comment_description = models.TextField(max_length=4000)
    
    # class Meta:
    #     db_table = '"CMS_HGC_CORE_MANAGEMNT"."LOCATIONS"'  # to be change to wherever we want locations to be
     
    def __str__(self):
        return str(self.location_name + ' [' + self.institution.name + ']' )

# ---------- Parts section

class Subdetector(ModelBase, Base):
    
    subdetector_id = models.AutoField(primary_key=True)
    subdetector_name = models.TextField(max_length=40)
    
    # class Meta: 
    #     managed = False
    #     db_table = '"CMS_HGC_CORE_CONSTRUCT"."SUBDETECTORS"'
    
    def __str__(self):
        return str(self.subdetector_name)

class Manufacturer(models.Model):
    
    manufacturer_id = models.IntegerField(primary_key=True)
    manufacturer_name = models.TextField(max_length=40, null=False)
    
    # class Meta:
    #     managed = False
    #     ordering = ('manufacturer_name',)
    #     db_table = '"CMS_HGC_CORE_CONSTRUCT"."MANUFACTURERS"'


class Part(models.Model):

    part_id = models.AutoField(primary_key=True)
    kind_of_part = models.ForeignKey('KindOfPart', on_delete=models.PROTECT, null=False, related_name='parts')
    location = models.ForeignKey('Location', on_delete=models.PROTECT, null=True, related_name='parts')
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.PROTECT, null=True, blank=True)
    name_label = models.TextField(max_length=40, null=True, blank=True)
    serial_number = models.TextField(max_length=40, null=True, blank=True)
    barcode = models.TextField(max_length=40, null=True, blank=True, unique=True)
    version = models.TextField(max_length=40, null=True, blank=True)
    installed_date = models.DateField(auto_now=False, blank=True)
    installed_by_user = models.TextField(max_length=40, null=True, blank=True)
    removed_date = models.DateField(auto_now=False, null=True, blank=True)
    removed_by_user = models.TextField(max_length=40, null=True, blank=True)
    extension_table_name = models.TextField(max_length=30, null=False, blank=True)
    record_insertion_time = models.DateTimeField(null=False, default=timezone.now)
    record_insertion_user = models.TextField(max_length=50, null=False)
    record_lastupdate_time = models.DateTimeField()
    record_lastupdate_user = models.TextField(max_length=50)
    comment_description = models.TextField(max_length=4000, null=False, blank=True)
    is_record_deleted = models.CharField(max_length=1, default='F', null=False)
    
    # class Meta:
    #     managed = False
    #     unique_together = ['serial_number', 'kind_of_part']
    #     db_table = '"CMS_HGC_CORE_CONSTRUCT"."PARTS"'

    def __str__(self):
        if self.serial_number:
            return str(self.serial_number)
        elif self.name_label:
            return str(self.name_label)
        elif self.barcode:
            return str(self.barcode)
        elif self.part_id:
            return str(self.part_id)
    
    # def connections(self):
    #     return PhysicalPartsTree.objects.filter(part_parent_id=self.part_id)


class KindOfPart(ModelBase):

    # class _KOPManager(models.Manager):
        
    #     def get_queryset(self):
    #         return super().get_queryset().select_related('subdetector', 'manufacturer').order_by('-kind_of_part_id')
        
    #     def order(self, field, order):
    #         if order == 'desc':
    #             f = Lower(field).desc()
    #         else:
    #             f = Lower(field).asc()
    #         return super().get_queryset().order_by(f, 'kind_of_part_id')

    # objects = _KOPManager()

    #kind_of_part_id = models.AutoField(primary_key=True)
    kind_of_part_id = models.IntegerField(primary_key = True, null = False)
    subdetector = models.ForeignKey('Subdetector', on_delete=models.CASCADE, null=True)
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.CASCADE, null=True)
    is_imaginary_part = models.CharField(max_length=1, default='F', null=False) # patikslinti
    display_name = models.CharField(max_length=40, null=False)
    is_detector_part = models.CharField(max_length=1, default='F', null=False) # patikslinti
    extension_table_name = models.TextField(max_length=30, null=False, default="PARTS")
    lpname = models.TextField(max_length=24)
    is_record_deleted = models.CharField(max_length=1, default='F', null=False)
    record_insertion_time = models.DateTimeField(null=False, default=timezone.now)
    record_insertion_user = models.TextField(max_length=50, null=False)
    record_lastupdate_time = models.DateTimeField()
    record_lastupdate_user = models.TextField(max_length=50)
    comment_description = models.TextField(max_length=4000)

    # class Meta:
    #     managed = False
    #     # ordering = ('display_name',)
    #     db_table = '"CMS_HGC_CORE_CONSTRUCT"."KINDS_OF_PARTS"'
    
    # def get_absolute_url(self):
    #     return reverse('part_edit', kwargs={'pk': self.pk})
    
    def __str__(self): 
        return str(self.display_name)



# ---------- Conditions section

class CondRun(models.Model):
    
    cond_run_id = models.IntegerField(primary_key=True)
    run_begin_timestamp = models.DateField(null=False)
    run_name = models.CharField(max_length=255)
    run_end_timestamp = models.DateField()
    initiated_by_user = models.CharField(max_length=80)
    location = models.CharField(max_length=40)
    run_type = models.CharField(max_length=120)
    run_number = models.IntegerField()
    is_record_deleted = models.CharField(max_length=1, default='F', null=False)
    record_insertion_time = models.DateTimeField(null=False, default=timezone.now)
    record_insertion_user = models.TextField(max_length=50, null=False)
    record_lastupdate_time = models.DateTimeField()
    record_lastupdate_user = models.TextField(max_length=50)

    # class Meta:
    #     managed = False
    #     app_label = 'construct'
    #     db_table = '"CMS_HGC_CORE_COND"."COND_RUNS"'

    def __str__(self):
        return str(self.run_name)

class KindOfCondition(models.Model):

    kind_of_condition_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40)
    extension_table_name = models.CharField(max_length=30)
    is_record_deleted = models.CharField(max_length=1, default='F', null=False)
    record_insertion_time = models.DateTimeField(null=False, default=timezone.now)
    record_insertion_user = models.TextField(max_length=50, null=False)
    record_lastupdate_time = models.DateTimeField()
    record_lastupdate_user = models.TextField(max_length=50)
    category_name = models.CharField(max_length=40)

    # class Meta:
    #     managed = False
    #     # verbose_name = _("KindOfCondition")
    #     # verbose_name_plural = _("KindOfConditions")
    #     db_table = '"CMS_HGC_CORE_COND"."KINDS_OF_CONDITIONS"'

    def __str__(self):
        return self.name


class ConditionsDataSets(models.Model):

    # class _CondDataSetManager(models.Manager):

    #     def get_queryset(self):
    #         return super().get_queryset().select_related('part', 'cond_run', 'channel_map', 'kind_of_condition')

    # objects = _CondDataSetManager()

    condition_data_set_id = models.IntegerField(primary_key=True)
    part = models.ForeignKey('Part', on_delete=models.PROTECT, related_name='conditions')
    # cond_run = models.ForeignKey('CondRun', on_delete=models.PROTECT, null=False)
    # channel_map = models.ForeignKey('ChannelMapsBase', on_delete=models.PROTECT, null=True)
    kind_of_condition = models.ForeignKey('KindOfCondition', on_delete=models.PROTECT, null=False)
    aggregated_cond_data_set = models.ForeignKey('self', on_delete=models.PROTECT)
    record_del_flag_time = models.DateTimeField()
    record_del_flag_user =  models.CharField(max_length=50)
    extension_table_name = models.CharField(max_length=30, null=False)
    data_file_name = models.CharField(max_length=4000)
    image_file_name = models.CharField(max_length=4000)
    version = models.CharField(max_length=40)
    create_timestamp = models.DateTimeField()
    created_by_user = models.CharField(max_length=50)
    subversion = models.IntegerField()
    number_of_events_in_set = models.IntegerField()
    set_number = models.IntegerField()
    set_begin_timestamp = models.DateTimeField()
    set_end_timestamp = models.DateTimeField()
    set_status = models.IntegerField()
    is_record_deleted = models.CharField(max_length=1, default='F', null=False)
    record_insertion_time = models.DateTimeField(null=False, default=timezone.now)
    record_insertion_user = models.TextField(max_length=50, null=False)

    # class Meta:
    #     # verbose_name = _("conditionsdataset")
    #     # verbose_name_plural = _("conditionsdatasets")
    #     db_table = '"CMS_HGC_CORE_COND"."COND_DATA_SETS"'

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("conditionsdatasets_detail", kwargs={"pk": self.pk})



# ---------- QC/User conditions section


class HGCROCTest(models.Model):

    record_id              = models.IntegerField(primary_key=True)
    condition_data_set_id = models.ForeignKey('ConditionsDataSets',on_delete=models.PROTECT, null=False)
    hgcroc_status          = models.CharField(max_length=12)
    comments               = models.CharField(max_length=100)
    
    # class Meta:
    #     # verbose_name = _("hgcroc-test")
    #     # verbose_name_plural = _("hgcroc-tests")
    #     # app_label = 'construct'
    #     db_table = '"CMS_HGC_HGCAL_COND"."HGCROC_TEST"'

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})