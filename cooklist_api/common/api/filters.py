from django_filters import NumberFilter, BaseInFilter


class NumberInFilter(BaseInFilter, NumberFilter):
    pass
