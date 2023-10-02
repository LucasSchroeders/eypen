from datetime import date, datetime, timedelta
from django import template

from users.choices import (
    BUSINESS_AREAS_CHOICES,
    SENIORITY_CHOICES,
    JOB_MODALITY,
    JOB_TYPE,
    VULNERABILITIES_CHOICES,
    GENDER_CHOICES,
    ETHNICITY_CHOICES,
    DISABLED_CHOICES,
)

register = template.Library()


@register.filter
def display_business_area(value):
    for k, v in BUSINESS_AREAS_CHOICES:
        if k == value:
            return v


@register.filter
def display_seniority(value):
    for k, v in SENIORITY_CHOICES:
        if k == value:
            return v


@register.filter
def display_job_modality(value):
    for k, v in JOB_MODALITY:
        if k == value:
            return v


@register.filter
def display_job_type(value):
    for k, v in JOB_TYPE:
        if k == value:
            return v
        

@register.filter
def display_vulnerabilities(value):
    for k, v in VULNERABILITIES_CHOICES:
        if k == value:
            return v


@register.filter
def display_gender(value):
    for k, v in GENDER_CHOICES:
        if k == value:
            return v


@register.filter
def display_disabled(value):
    for k, v in DISABLED_CHOICES:
        if k == value:
            return v


@register.filter
def display_ethnicity(value):
    for k, v in ETHNICITY_CHOICES:
        if k == value:
            return v


@register.filter
def filter_step(value, attr):
    result = value.filter(**eval(attr)).first()
    return result.step


@register.filter
def filter_notifications(value):
    yesterday = datetime.now() - timedelta(days=1)
    result = value.filter(created_at__gte=yesterday).order_by('created_at')
    return result


@register.filter
def filter_age(value):
    today = date.today() 
    return today.year - value.year - ((today.month, today.day) < (value.month, value.day)) 
