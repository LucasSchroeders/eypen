from django.views.generic import TemplateView
from rest_framework.decorators import permission_classes

from users.permission import AllowOnlyApplicant


@permission_classes((AllowOnlyApplicant,))
class NotificationTemplateView(TemplateView):
    template_name = 'users/profile/notifications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.profile 

        context['profile_user'] = profile
        context['notifications'] = profile.notifications.order_by('created_at')

        return context