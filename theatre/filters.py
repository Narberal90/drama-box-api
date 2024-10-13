import django_filters

from .models import Play, Performance


class MultipleValuesCapitalizeFilter(
    django_filters.BaseInFilter, django_filters.CharFilter
):
    def filter(self, qs, values):
        if not values:
            return qs
        values = [value.strip().capitalize() for value in values]
        return super().filter(qs, values)


class PlayFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    duration_min = django_filters.NumberFilter(field_name="duration", lookup_expr="gte")
    duration_max = django_filters.NumberFilter(field_name="duration", lookup_expr="lte")

    class Meta:
        model = Play
        fields = ["title", "genres", "actors", "duration_min", "duration_max"]


class PerformanceFilter(django_filters.FilterSet):
    show_time_min = django_filters.DateTimeFilter(field_name="show_time", lookup_expr="gte")
    show_time_max = django_filters.DateTimeFilter(field_name="show_time", lookup_expr="lte")

    class Meta:
        model = Performance
        fields = ["play__title", "theatre_hall", "show_time_min", "show_time_max"]
