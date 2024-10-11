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
    genre = MultipleValuesCapitalizeFilter(field_name="genre__name")
    actor = MultipleValuesCapitalizeFilter(field_name="actor__last_name")
    duration_min = django_filters.NumberFilter(field_name="duration", lookup_expr="gte")
    duration_max = django_filters.NumberFilter(field_name="duration", lookup_expr="lte")

    class Meta:
        model = Play
        fields = ["title", "genre", "actor", "duration_min", "duration_max"]


class PerformanceFilter(django_filters.FilterSet):
    play_title = django_filters.CharFilter(field_name="play__title", lookup_expr="icontains")
    theatre_hall = MultipleValuesCapitalizeFilter(field_name="theatre_hall__name")
    show_time_min = django_filters.DateTimeFilter(field_name="show_time", lookup_expr="gte")
    show_time_max = django_filters.DateTimeFilter(field_name="show_time", lookup_expr="lte")

    class Meta:
        model = Performance
        fields = ["play_title", "theatre_hall", "show_time_min", "show_time_max"]