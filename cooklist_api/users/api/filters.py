from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from rest_framework_filters import FilterSet, filters


class UserFilter(FilterSet):
    search__icontains = filters.CharFilter(method="search")

    class Meta:
        model = User
        fields = {
            "first_name": ["exact", "in", "contains", "icontains"],
            "last_name": ["exact", "in", "contains", "icontains"],
            "username": ["exact", "in", "contains", "icontains"],
            "email": ["exact", "in", "contains", "icontains"],
        }

    def search(self, queryset, field, value):
        if value:
            return queryset.annotate(
                search=SearchVector("username", "first_name", "last_name", "email")
            ).filter(Q(search__icontains=value) | Q(search=value))
        return queryset
