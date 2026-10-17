from django.urls import reverse
from django.utils.translation import get_language

from .models import Profile, SocialLink


def language(request):
    code = (get_language() or 'fa').split('-')[0]
    profile = Profile.objects.first()
    return {
        'CURRENT_LANG': code,
        'HTML_LANG': code,
        'HTML_DIR': 'rtl' if code == 'fa' else 'ltr',
        'IS_RTL': code == 'fa',
        'HOME_URL': reverse('my_cv:index'),
        'nav_profile': profile,
        'nav_social_links': SocialLink.objects.all(),
    }
