import base64
import mimetypes
from pathlib import Path

from django.conf import settings
from django.contrib.staticfiles import finders
from django.contrib import messages
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render

from .geo import client_ip

from .forms import ContactForm
from .i18n import t
from .models import (
    Certificate,
    Experience,
    Profile,
    Project,
    Skill,
    SkillCategory,
    ServiceCard,
    SocialLink,
)


def _shared_context(request, form=None):
    profile = Profile.objects.first()
    skill_categories = SkillCategory.objects.prefetch_related('skills').all()
    return {
        'profile': profile,
        'skill_categories': skill_categories,
        'projects': Project.objects.prefetch_related('skills', 'images'),
        'experiences': Experience.objects.all(),
        'certificates': Certificate.objects.all(),
        'social_links': SocialLink.objects.all(),
        'service_cards': ServiceCard.objects.filter(is_visible=True),
        'contact_form': form or ContactForm(),
        'years_experience': 4,
        # Public portfolio is smaller; total delivered work is shown as 20+.
        'project_count': 20,
        'certificate_count': Certificate.objects.count(),
        'skill_count': Skill.objects.filter(featured=True).count(),
        'top_skills': Skill.objects.filter(featured=True).order_by('-level', 'order')[:6],
    }


def _contact_limited(request):
    """At most 5 real messages per hour from one address."""
    ip = client_ip(request) or 'unknown'
    key = f'contact-rate:{ip}'
    count = cache.get(key, 0)
    if count >= 5:
        return True
    cache.set(key, count + 1, 3600)
    return False


def index_view(request):
    if request.method == 'POST':
        # Bots that fill the hidden field get the same reply as a real send.
        if (request.POST.get('website') or '').strip():
            messages.success(request, t('contact.success'))
            return redirect(f"{request.path}#contact")
        form = ContactForm(request.POST)
        if form.is_valid():
            if _contact_limited(request):
                messages.error(request, t('contact.limited'))
                return redirect(f"{request.path}#contact")
            msg = form.save()
            profile = Profile.objects.first()
            to_email = (profile.email if profile and profile.email else '') or settings.DEFAULT_FROM_EMAIL
            subject = ' '.join((msg.subject or '').split())[:180] or 'Message'
            try:
                if to_email:
                    send_mail(
                        subject=f'[CV] {subject}',
                        message=f'{msg.name} <{msg.email}>\n\n{msg.message}',
                        from_email=settings.DEFAULT_FROM_EMAIL or None,
                        recipient_list=[to_email],
                        fail_silently=True,
                    )
            except Exception:
                pass
            messages.success(request, t('contact.success'))
            return redirect(f"{request.path}#contact")
        messages.error(request, t('contact.error'))
        return render(request, 'website/index.html', _shared_context(request, form))
    return render(request, 'website/index.html', _shared_context(request))


def resume_view(request):
    return render(request, 'website/resume.html', _shared_context(request))


def _photo_data_uri(profile):
    """Embed the admin photo, or the public site portrait when none is uploaded."""
    raw = b''
    name = ''
    if profile and profile.photo:
        try:
            with profile.photo.open('rb') as handle:
                raw = handle.read()
            name = profile.photo.name
        except Exception:
            raw = b''
    if not raw:
        found = finders.find('snapfolio/img/profile/profile-2.webp')
        if found:
            name = found
            raw = Path(found).read_bytes()
    if not raw:
        return ''
    mime = mimetypes.guess_type(name)[0] or 'image/webp'
    return f'data:{mime};base64,{base64.b64encode(raw).decode("ascii")}'


def resume_download_view(request):
    """Two-page A4 resume, rendered from the current admin data."""
    preview = request.GET.get('view') == '1'
    context = _shared_context(request)
    context['photo_data_uri'] = _photo_data_uri(context['profile'])
    response = render(request, 'website/resume_a4.html', context)
    if not preview:
        response['Content-Disposition'] = 'attachment; filename="Mohammad-Eskandarloo-CV.html"'
    return response


def project_detail_view(request, slug):
    project = get_object_or_404(Project.objects.prefetch_related('skills', 'images'), slug=slug)
    return render(request, 'website/project_detail.html', {
        'project': project,
        'profile': Profile.objects.first(),
    })


def ai_chat_view(request):
    ai_chat_view = {
        'name': 'محمد اسکندرلو',
        'phone_number': '+989337315709',
        'email': 'mohammad.eska34@gmail.com',
    }
    return render(request, 'website/ai_chat_view.html', ai_chat_view)


def decoy_admin_view(request):
    # Friendly decoy for the old /admin/ path. The real admin lives elsewhere.
    return render(request, 'website/decoy_admin.html')
