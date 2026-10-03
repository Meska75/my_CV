from django.db import models
from django.utils.text import slugify
from django.utils.translation import get_language


def _unicode_slug(value):
    """Slugify keeping Persian characters readable in URLs."""
    return slugify(value, allow_unicode=True)


def current_lang():
    return (get_language() or 'fa').split('-')[0]


class TranslatableMixin:
    """Read `{field}_en` when the active language is English."""

    def loc(self, field):
        if current_lang() == 'en':
            value = getattr(self, f'{field}_en', None)
            if value:
                return value
        return getattr(self, field) or ''


class Profile(TranslatableMixin, models.Model):
    """Single-row site identity / hero content."""

    full_name = models.CharField('نام کامل', max_length=120)
    full_name_en = models.CharField('Full name (EN)', max_length=120, blank=True)
    headline = models.CharField('عنوان شغلی', max_length=160,
                                help_text='مثلاً: مهندس بک‌اند پایتون و هوش مصنوعی')
    headline_en = models.CharField('Headline (EN)', max_length=160, blank=True)
    tagline = models.CharField('شعار کوتاه', max_length=255, blank=True)
    tagline_en = models.CharField('Tagline (EN)', max_length=255, blank=True)
    about = models.TextField('درباره‌ی من', blank=True)
    about_en = models.TextField('About (EN)', blank=True)
    location = models.CharField('محل سکونت', max_length=120, blank=True)
    location_en = models.CharField('Location (EN)', max_length=120, blank=True)
    email = models.EmailField('ایمیل', blank=True)
    phone = models.CharField('تلفن', max_length=40, blank=True)
    show_phone = models.BooleanField('نمایش عمومی تلفن', default=False)
    photo = models.ImageField('عکس', upload_to='profile/', blank=True, null=True)
    resume_file = models.FileField('فایل رزومه', upload_to='resume/', blank=True, null=True)
    available_for_work = models.BooleanField('آماده‌ی همکاری', default=True)

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل'

    def __str__(self):
        return self.full_name

    @property
    def display_name(self):
        return self.loc('full_name') or self.full_name

    @property
    def first_name(self):
        parts = self.display_name.split()
        return parts[0] if parts else self.display_name

    @property
    def last_name(self):
        parts = self.display_name.split()
        return ' '.join(parts[1:]) if len(parts) > 1 else ''


class SocialLink(models.Model):
    """Social / contact links shown in the contact section and footer."""

    label = models.CharField('عنوان', max_length=60)
    url = models.URLField('لینک')
    icon = models.CharField('کلاس آیکن', max_length=60, blank=True,
                            help_text='مثلاً: fab fa-github')
    order = models.PositiveIntegerField('ترتیب', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'لینک اجتماعی'
        verbose_name_plural = 'لینک‌های اجتماعی'

    def __str__(self):
        return self.label

    @property
    def bootstrap_icon(self):
        mapping = {
            'github': 'bi-github',
            'linkedin': 'bi-linkedin',
            'email': 'bi-envelope',
            'mail': 'bi-envelope',
            'twitter': 'bi-twitter-x',
            'x': 'bi-twitter-x',
            'instagram': 'bi-instagram',
            'telegram': 'bi-telegram',
            'whatsapp': 'bi-whatsapp',
        }
        key = (self.label or '').strip().lower()
        if key in mapping:
            return mapping[key]
        icon = (self.icon or '').lower()
        for token, bi in mapping.items():
            if token in icon:
                return bi
        return 'bi-link-45deg'


class SkillCategory(TranslatableMixin, models.Model):
    name = models.CharField('نام دسته', max_length=80)
    name_en = models.CharField('Category name (EN)', max_length=80, blank=True)
    slug = models.SlugField('اسلاگ', max_length=90, unique=True, blank=True, allow_unicode=True)
    icon = models.CharField('کلاس آیکن', max_length=60, blank=True)
    order = models.PositiveIntegerField('ترتیب', default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'دسته‌ی مهارت'
        verbose_name_plural = 'دسته‌های مهارت'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _unicode_slug(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Skill(TranslatableMixin, models.Model):
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE,
                                 related_name='skills', verbose_name='دسته')
    name = models.CharField('نام مهارت', max_length=80)
    name_en = models.CharField('Skill name (EN)', max_length=80, blank=True)
    level = models.PositiveSmallIntegerField('سطح (۱ تا ۵)', default=3)
    featured = models.BooleanField('نمایش در بخش مهارت‌ها', default=True,
                                   help_text='اگر خاموش باشد فقط به‌عنوان تگ پروژه استفاده می‌شود.')
    order = models.PositiveIntegerField('ترتیب', default=0)

    class Meta:
        ordering = ['category__order', 'order', 'name']
        verbose_name = 'مهارت'
        verbose_name_plural = 'مهارت‌ها'

    def __str__(self):
        return self.name

    @property
    def percent(self):
        # Cap below 100 so bars read as strong but not exaggerated.
        mapping = {1: 48, 2: 62, 3: 74, 4: 84, 5: 92}
        return mapping.get(int(self.level), 70)


class Experience(TranslatableMixin, models.Model):
    role = models.CharField('عنوان شغلی', max_length=160)
    role_en = models.CharField('Role (EN)', max_length=160, blank=True)
    organization = models.CharField('سازمان', max_length=160)
    organization_en = models.CharField('Organization (EN)', max_length=160, blank=True)
    location = models.CharField('مکان', max_length=120, blank=True)
    location_en = models.CharField('Location (EN)', max_length=120, blank=True)
    period = models.CharField('بازه‌ی زمانی', max_length=120,
                              help_text='متن نمایشی، مثلاً: خرداد ۱۴۰۲ – اکنون')
    period_en = models.CharField('Period (EN)', max_length=120, blank=True)
    start_date = models.DateField('تاریخ شروع (برای مرتب‌سازی)', null=True, blank=True)
    is_current = models.BooleanField('شغل فعلی', default=False)
    description = models.TextField('توضیحات', blank=True)
    description_en = models.TextField('Description (EN)', blank=True)
    order = models.PositiveIntegerField('ترتیب', default=0)

    class Meta:
        ordering = ['order', '-start_date']
        verbose_name = 'تجربه‌ی کاری'
        verbose_name_plural = 'تجربه‌های کاری'

    def __str__(self):
        return f'{self.role} — {self.organization}'


class Project(TranslatableMixin, models.Model):
    class Category(models.TextChoices):
        AI = 'ai', 'هوش مصنوعی'
        BACKEND = 'backend', 'بک‌اند'
        DATA = 'data', 'داده'
        WEB = 'web', 'وب'

    CATEGORY_EN = {
        'ai': 'Artificial Intelligence',
        'backend': 'Backend',
        'data': 'Data',
        'web': 'Web',
    }

    class Status(models.TextChoices):
        COMPLETED = 'completed', 'تکمیل‌شده'
        IN_PROGRESS = 'in_progress', 'در حال توسعه'

    STATUS_EN = {
        'completed': 'Completed',
        'in_progress': 'In progress',
    }

    title = models.CharField('عنوان', max_length=160)
    title_en = models.CharField('Title (EN)', max_length=160, blank=True)
    slug = models.SlugField('اسلاگ', max_length=180, unique=True, blank=True, allow_unicode=True)
    summary = models.CharField('خلاصه‌ی یک‌خطی', max_length=255)
    summary_en = models.CharField('Summary (EN)', max_length=255, blank=True)
    problem = models.TextField('مشکل', blank=True)
    problem_en = models.TextField('Problem (EN)', blank=True)
    solution = models.TextField('راه‌حل', blank=True)
    solution_en = models.TextField('Solution (EN)', blank=True)
    outcome = models.TextField('نتیجه', blank=True)
    outcome_en = models.TextField('Outcome (EN)', blank=True)
    category = models.CharField('دسته', max_length=20, choices=Category.choices, default=Category.BACKEND)
    status = models.CharField('وضعیت', max_length=20, choices=Status.choices, default=Status.COMPLETED)
    skills = models.ManyToManyField(Skill, related_name='projects', blank=True, verbose_name='تک‌استک')
    cover_image = models.ImageField('تصویر کاور', upload_to='projects/', blank=True, null=True)
    github_url = models.URLField('لینک گیت‌هاب', blank=True)
    live_url = models.URLField('لینک زنده', blank=True)
    is_private = models.BooleanField('پروژه‌ی خصوصی (بدون افشای کد)', default=False)
    is_featured = models.BooleanField('شاخص', default=False)
    order = models.PositiveIntegerField('ترتیب', default=0)

    class Meta:
        ordering = ['order', '-is_featured']
        verbose_name = 'پروژه'
        verbose_name_plural = 'پروژه‌ها'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _unicode_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def category_label(self):
        if current_lang() == 'en':
            return self.CATEGORY_EN.get(self.category, self.category)
        return self.get_category_display()

    def status_label(self):
        if current_lang() == 'en':
            return self.STATUS_EN.get(self.status, self.status)
        return self.get_status_display()

    @property
    def placeholder_image(self):
        mapping = {
            'ai': 'snapfolio/img/portfolio/portfolio-1.webp',
            'backend': 'snapfolio/img/portfolio/portfolio-2.webp',
            'data': 'snapfolio/img/portfolio/portfolio-7.webp',
            'web': 'snapfolio/img/portfolio/portfolio-10.webp',
        }
        return mapping.get(self.category, 'snapfolio/img/portfolio/portfolio-5.webp')


class Certificate(TranslatableMixin, models.Model):
    class Category(models.TextChoices):
        BACKEND = 'backend', 'بک‌اند'
        AI_DATA = 'ai_data', 'هوش مصنوعی و داده'
        OTHER = 'other', 'سایر'

    CATEGORY_EN = {
        'backend': 'Backend',
        'ai_data': 'AI & Data',
        'other': 'Other',
    }

    title = models.CharField('عنوان دوره', max_length=200)
    title_en = models.CharField('Title (EN)', max_length=200, blank=True)
    issuer = models.CharField('برگزارکننده', max_length=160, blank=True)
    issuer_en = models.CharField('Issuer (EN)', max_length=160, blank=True)
    instructor = models.CharField('مدرس', max_length=120, blank=True)
    instructor_en = models.CharField('Instructor (EN)', max_length=120, blank=True)
    year = models.CharField('سال', max_length=20, blank=True)
    year_en = models.CharField('Year (EN)', max_length=20, blank=True)
    hours = models.PositiveIntegerField('ساعت', null=True, blank=True)
    category = models.CharField('دسته', max_length=20, choices=Category.choices, default=Category.OTHER)
    url = models.URLField('لینک مدرک', blank=True)
    image = models.ImageField('تصویر مدرک', upload_to='certificates/', blank=True, null=True)
    order = models.PositiveIntegerField('ترتیب', default=0)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'گواهینامه'
        verbose_name_plural = 'گواهینامه‌ها'

    def __str__(self):
        return self.title

    def category_label(self):
        if current_lang() == 'en':
            return self.CATEGORY_EN.get(self.category, self.category)
        return self.get_category_display()


class ContactMessage(models.Model):
    name = models.CharField('نام', max_length=120)
    email = models.EmailField('ایمیل')
    subject = models.CharField('موضوع', max_length=200)
    message = models.TextField('پیام')
    created_at = models.DateTimeField('تاریخ', auto_now_add=True)
    is_read = models.BooleanField('خوانده‌شده', default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'پیام تماس'
        verbose_name_plural = 'پیام‌های تماس'

    def __str__(self):
        return f'{self.name} — {self.subject}'
