from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactForm
from .i18n import t
from .models import (
    Certificate,
    Experience,
    Profile,
    Project,
    Skill,
    SkillCategory,
    SocialLink,
)


def _shared_context(request, form=None):
    profile = Profile.objects.first()
    skill_categories = SkillCategory.objects.prefetch_related('skills').all()
    return {
        'profile': profile,
        'skill_categories': skill_categories,
        'projects': Project.objects.exclude(live_url='').prefetch_related('skills'),
        'experiences': Experience.objects.all(),
        'certificates': Certificate.objects.all(),
        'social_links': SocialLink.objects.all(),
        'contact_form': form or ContactForm(),
        'years_experience': 4,
        # Public portfolio is smaller; total delivered work is shown as 20+.
        'project_count': 20,
        'certificate_count': Certificate.objects.count(),
        'skill_count': Skill.objects.filter(featured=True).count(),
        'top_skills': Skill.objects.filter(featured=True).order_by('-level', 'order')[:6],
    }


def index_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save()
            profile = Profile.objects.first()
            to_email = (profile.email if profile and profile.email else '') or settings.DEFAULT_FROM_EMAIL
            try:
                if to_email:
                    send_mail(
                        subject=f'[CV] {msg.subject}',
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


def project_detail_view(request, slug):
    project = get_object_or_404(Project.objects.prefetch_related('skills'), slug=slug)
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
