from django.db import models

CassetteNames = [
    ('CEE01', 'CEE01'),
    ('CEE02', 'CEE02'),
    ('CEE03', 'CEE03'),
    ('CEE04', 'CEE04'),
    ('CEE05', 'CEE05'),
    ('CEE06', 'CEE06'),
    ('CEE07', 'CEE07'),
    ('CEE08', 'CEE08'),
    ('CEE09', 'CEE09'),
    ('CEE10', 'CEE10'),
    ('CEE11', 'CEE11'),
    ('CEE12', 'CEE12'),
    ('CEE13', 'CEE13'),    
]

# Create your models here.

class Workstation(models.Model):
    name = models.CharField(max_length=50, null=True)
    cassette = models.OneToOneField('Cassette', on_delete=models.PROTECT, null=True, blank=True, related_name="workstation_cassette")
    def __str__(self):
        return str(self.name)
    def get_absolute_url(self):
        return ""
    
class Step(models.Model):
    name = models.IntegerField(default=1)
    details = models.CharField(max_length=100, null=True)
    parts = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return str(self.name)

class Cassette(models.Model):
    #name = models.CharField(max_length=50, null=True)
    name = models.CharField(choices=CassetteNames, null=True, max_length=50)
    step = models.IntegerField(default=1)
    workstation = models.OneToOneField('Workstation', on_delete=models.PROTECT, null=True, blank=True, related_name="cassette_workstation")
    barcode = models.IntegerField(null=True, blank=True)
    side = models.CharField(max_length=50, default="1")
    started = models.BooleanField(default="False")
    def __str__(self):
        return str(self.name)
    def get_absolute_url(self):
        return ""

class Part(models.Model):
    name = models.CharField(max_length=50, null=True)
    barcode = models.IntegerField(null=True, blank=True)
    cassette = models.ForeignKey('Cassette', on_delete=models.PROTECT, null=True)
    module = models.ForeignKey('Modulemap', on_delete=models.PROTECT, null=True)
    type = models.CharField(max_length=50, null=True)
    placed = models.BooleanField(default = False)
    def __str__(self):
        return str(self.id)
    def get_absolute_url(self):
        return "list"


class Modulemap(models.Model):
    plane = models.CharField(max_length=50, null=True)
    u = models.CharField(max_length=50, null=True)
    v = models.CharField(max_length=50, null=True)
    itype = models.CharField(max_length=50, null=True)
    x0 = models.CharField(max_length=50, null=True)
    y0 = models.CharField(max_length=50, null=True)
    irot = models.CharField(max_length=50, null=True)
    nvertices = models.CharField(max_length=50, null=True)
    vx_0 = models.CharField(max_length=50, null=True)
    vy_0 = models.CharField(max_length=50, null=True)
    vx_1 = models.CharField(max_length=50, null=True)
    vy_1 = models.CharField(max_length=50, null=True)
    vx_2 = models.CharField(max_length=50, null=True)
    vy_2 = models.CharField(max_length=50, null=True)
    vx_3 = models.CharField(max_length=50, null=True)
    vy_3 = models.CharField(max_length=50, null=True)
    vx_4 = models.CharField(max_length=50, null=True)
    vy_4 = models.CharField(max_length=50, null=True)
    vx_5 = models.CharField(max_length=50, null=True)
    vy_5 = models.CharField(max_length=50, null=True)
    vx_6 = models.CharField(max_length=50, null=True)
    vy_6 = models.CharField(max_length=50, null=True)
    icassette = models.CharField(max_length=50, null=True)
    trigRate = models.CharField(max_length=50, null=True)
    trigLinks = models.CharField(max_length=50, null=True)
    dataRate_ld = models.CharField(max_length=50, null=True)
    dataLinks_ld = models.CharField(max_length=50, null=True)
    dataRate_hd = models.CharField(max_length=50, null=True)
    dataLinks_hd = models.CharField(max_length=50, null=True)
    MB = models.CharField(max_length=50, null=True)
    wagon = models.CharField(max_length=50, null=True)
    isEngine = models.CharField(max_length=50, null=True)
    nROCs = models.CharField(max_length=50, null=True)
    power = models.CharField(max_length=50, null=True)
    mrot = models.CharField(max_length=50, null=True)
    phi = models.CharField(max_length=50, null=True)
    HDorLD = models.CharField(max_length=50, null=True)
    hash = models.CharField(max_length=50, null=True)
    hash_hdld = models.CharField(max_length=50, null=True)
    dataPp0 = models.CharField(max_length=50, null=True)
    trigPp0 = models.CharField(max_length=50, null=True)
    dataPp0_type = models.CharField(max_length=50, null=True)
    trigPp0_type = models.CharField(max_length=50, null=True)
    dataPp1 = models.CharField(max_length=50, null=True)
    trigPp1 = models.CharField(max_length=50, null=True)
    dataPp1_type = models.CharField(max_length=50, null=True)
    trigPp1_type = models.CharField(max_length=50, null=True)
    
