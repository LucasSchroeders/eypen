from rest_framework import permissions


class AllowOnlyCompany(permissions.BasePermission):
    """
    Global permission check for company users.
    """

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.profile.is_company
    

class AllowOnlyApplicant(permissions.BasePermission):
    """
    Global permission check for applicant users.
    """

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.profile.is_applicant
