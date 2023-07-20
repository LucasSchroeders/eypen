from django.contrib import admin

from .models import Profile, Experience, AcademicFormation, Competence
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'full_name',
        'cpf',
    )
    search_fields = ('user__email', 'cpf')
    list_filter = (
        'is_disabled',
    )
    readonly_fields = ('user',)

    def get_queryset(self, request):
        return super().get_queryset(request)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        # 'profile__full_name',
        'position',
        'company',
        'business_area'
    )
    search_fields = ('profile__user__email', 'profile__cpf')
    list_filter = (
        'is_working',
    )
    readonly_fields = ('profile',)

    def get_queryset(self, request):
        return super().get_queryset(request)


@admin.register(AcademicFormation)
class AcademicFormationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
    )
    search_fields = ('profile__user__email', 'profile__cpf')
    # list_filter = (
    #     'is_working',
    # )
    readonly_fields = ('profile',)

    def get_queryset(self, request):
        return super().get_queryset(request)


@admin.register(Competence)
class CompetenceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        # 'profile__full_name',
        # 'position',
        # 'company',
        # 'business_area'
    )
    search_fields = ('profile__user__email', 'profile__cpf')
    # list_filter = (
    #     'is_working',
    # )
    readonly_fields = ('profile',)

    def get_queryset(self, request):
        return super().get_queryset(request)
    