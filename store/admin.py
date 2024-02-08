from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models import Q

from .models import BookInventory


class InStockFilter(SimpleListFilter):
    title = 'In Stock'
    parameter_name = 'filter_in_stock'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Yes'),
            ('no', 'No')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(Q(quantity_in_hand__gte=1) | Q(quantity_to_be_delivered__gte=1))
        if self.value() == 'no':
            return queryset.filter(quantity_in_hand__lte=0, quantity_to_be_delivered__lte=0)


@admin.register(BookInventory)
class BookInventory(admin.ModelAdmin):
    list_display = ['book', 'quantity_in_hand', 'quantity_to_be_delivered',
                    'in_stock', 'pre_order']
    list_filter = [InStockFilter]
