from django.contrib import admin

from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'cnpj',
    )
    search_fields = ('name', 'cnpj')

    def get_queryset(self, request):
        return super().get_queryset(request)
