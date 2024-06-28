from django_filters import rest_framework as filters, DateFromToRangeFilter

from .models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    # TODO: задайте требуемые фильтры
    # creator = filters.NumberFilter(field_name='id')

    created_at = DateFromToRangeFilter()

    # status = filters.CharFilter(field_name='status')

    class Meta:
        model = Advertisement
        fields = ['creator', 'created_at', 'status']