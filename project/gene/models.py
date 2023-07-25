from django.db import models
from gene.constants import CarrierType, GeneCategory
from gene.utils import generate_icon_path, generate_color
from django.contrib.auth import models as auth_models

class Colony(models.Model):
    user = models.ForeignKey(auth_models.User, null=True, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=100)

    def __str__(self):
        return self.name


class XenoTypeManager(models.Manager):
    pass


class XenoType(models.Model):
    objects = XenoTypeManager()
    label = models.CharField(null=False, max_length=12)
    vanilla = models.BooleanField(default=False)
    carrier_type = models.IntegerField(null=False, choices=CarrierType.choices)
    gene_set = models.ManyToManyField('gene.Gene', related_name='xenotype_set')

    @property
    def icon(self):
        return 'xenotype_icons/%s.png' % self.label

    def __str__(self):
        return self.label.title()


class GeneManager(models.Manager):
    pass


class Gene(models.Model):
    objects = GeneManager()
    label = models.CharField(max_length=50)
    def_name = models.CharField(max_length=50)
    vanilla = models.BooleanField(default=False)
    category = models.CharField(choices=GeneCategory.choices, null=False, max_length=30)
    icon = models.CharField(max_length=150, default=None, null=True)
    color = models.CharField(max_length=50, default=None, null=True)
    
    def save(self, *args, **kwargs):
        # reset icon and color if blank for whatever reason
        self.icon = self.icon or generate_icon_path(self)
        self.color = self.color or generate_color(self)
        super(Gene, self).save(*args, **kwargs)

    def __str__(self):
        return self.label.title()


