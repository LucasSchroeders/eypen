from django.contrib import admin

from .models import Company, Vacancy, Step

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


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'job_position',
    )
    search_fields = ('job_position', 'company__name')
    readonly_fields = ('company',)

    def get_queryset(self, request):
        return super().get_queryset(request)


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'step',
        'title',
    )
    search_fields = ('title', 'vacancy__company__name')
    readonly_fields = ('vacancy',)

    def get_queryset(self, request):
        return super().get_queryset(request)
