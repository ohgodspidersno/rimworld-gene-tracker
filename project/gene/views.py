from django.shortcuts import render
from django.db.models import Count, Case, When, BooleanField
from django.views.generic import ListView
from rest_framework import viewsets, filters
from gene.models import Gene, XenoType, GeneCategory
from gene.serializers import GeneSerializer, XenoTypeSerializer
from pprint import pprint


class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    example from https://www.django-rest-framework.org/api-guide/filtering/
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)


class GeneViewSet(viewsets.ModelViewSet):
    queryset = Gene.objects.prefetch_related('xenotype_set').annotate(
        xenotype_count=Count('xenotype_set'),
        is_cosmetic=Case(
            When(
                category=GeneCategory.COSMETIC,
                then=1,
            ),
            default=0,
            output_field=BooleanField()
        )
    ).annotate(
        trader_only=Case(
            When(
                xenotype_count=0,
                then=1
            ),
            default=0,
            output_field=BooleanField()
        ),
    )
    serializer_class = GeneSerializer

    # def get_options(self):
    #     return "options", {
    #         "xenotype": [{'label': obj.label, 'value': obj.pk} for obj in XenoType.objects.all()],
    #         "gene": [{'label': obj.label, 'value': obj.pk} for obj in Gene.objects.all()]
    #     }
    #
    # class Meta:
    #     datatables_extra_json = ('get_options', )


class XenoTypeViewSet(viewsets.ModelViewSet):
    queryset = XenoType.objects.prefetch_related('gene_set').annotate(gene_count=Count('gene_set'))
    serializer_class = XenoTypeSerializer


class GeneCheckListView(ListView):
    template_name = 'gene/checklist.html'
    queryset = Gene.objects.prefetch_related('xenotype_set')
    xenotype_queryset = XenoType.objects.prefetch_related('gene_set')

    def get_context_data(self, *args, **kwargs):
        ctx = super(GeneCheckListView, self).get_context_data(*args, **kwargs)
        ctx['xenotype_list'] = self.xenotype_queryset.all()
        return ctx

