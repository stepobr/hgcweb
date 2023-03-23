from django.db import models


from base.models import Part


class VisualInspection(models.Model):
    record_id     = models.IntegerField(primary_key=True)
    pcb_id        = models.IntegerField(blank=True)
    test_date     = models.DateTimeField(blank=True)
    tested_by     = models.CharField(max_length=20, blank=True)
    stage         = models.CharField(max_length=20, blank=True)
    comments      = models.CharField(max_length=50, blank=True)
    flatness      = models.CharField(max_length=10, blank=True)
    thikness      = models.CharField(max_length=20, blank=True)
    plating_bga   = models.CharField(max_length=10, blank=True)
    plating_holes = models.CharField(max_length=10, blank=True)
    mask_aligment = models.CharField(max_length=10, blank=True)
    glue          = models.CharField(max_length=10, blank=True)
    accepted      = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.record_id
    
    class Meta:
        db_table = 'qc_pcb_visual'


