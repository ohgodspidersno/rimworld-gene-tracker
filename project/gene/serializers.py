from rest_framework import serializers
from gene.models import Gene, XenoType
from gene.constants import GeneCategory
from django.db import models
from django.db.models import Count, Case, When, BooleanField
from django.templatetags.static import static
from pprint import pprint


class FilterCosmeticListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        if isinstance(data, (models.Manager, models.QuerySet)):
            data = data.exclude(category=GeneCategory.COSMETIC)
        return super(FilterCosmeticListSerializer, self).to_representation(data)

class SortCosmeticLastSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        if isinstance(data, (models.Manager, models.QuerySet)):
            data = data.annotate(
                xenotype_count=Count('xenotype_set'),
                is_cosmetic=Case(
                    When(
                        category=GeneCategory.COSMETIC,
                        then=1,
                    ),
                    default=0,
                    output_field=BooleanField()
                )
            ).order_by('is_cosmetic', '-category', 'label')
        return super(SortCosmeticLastSerializer, self).to_representation(data)


class PartialXenoTypeSerializer(serializers.ModelSerializer):
    label = serializers.CharField(read_only=True)

    class Meta:
        model = XenoType
        fields = (
            'label',
        )

class CategorySerializer(serializers.CharField):
    def to_representation(self, value):
        return dict(GeneCategory.choices).get(value)

class GeneSerializer(serializers.ModelSerializer):
    label = serializers.CharField(read_only=True)
    def_name = serializers.CharField(read_only=True)
    icon = serializers.CharField(read_only=True)
    xenotype_set = PartialXenoTypeSerializer(read_only=True, many=True)
    color = serializers.CharField(read_only=True)
    xenotype_count = serializers.IntegerField(read_only=True)
    category = CategorySerializer(read_only=True)
    is_cosmetic = serializers.BooleanField(read_only=True)
    trader_only = serializers.BooleanField(read_only=True)

    class Meta:
        model = Gene
        fields = (
            'label', 'def_name', 'icon', 'xenotype_set', 'color', 'xenotype_count', 'category',
            'is_cosmetic', 'trader_only',
        )


class PartialGeneSerializer(serializers.ModelSerializer):
    label = serializers.CharField(read_only=True)
    def_name = serializers.CharField(read_only=True)
    icon = serializers.CharField(read_only=True)
    color = serializers.CharField(read_only=True)
    category = serializers.CharField(read_only=True)
    is_cosmetic = serializers.BooleanField(read_only=True)

    class Meta(GeneSerializer.Meta):
        model = Gene
        list_serializer_class = SortCosmeticLastSerializer
        fields = (
            'label', 'def_name', 'icon', 'color', 'category', 'is_cosmetic',
        )


class XenoTypeSerializer(serializers.ModelSerializer):
    label = serializers.CharField(read_only=True)
    gene_set = PartialGeneSerializer(read_only=True, many=True)
    gene_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = XenoType
        fields = (
            'label', 'gene_set', 'gene_count',
        )



