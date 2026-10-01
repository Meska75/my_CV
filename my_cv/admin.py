from django.contrib import admin

from unfold.admin import ModelAdmin, TabularInline

from .models import (
    Certificate,
    ContactMessage,
    Experience,
    Profile,
    Project,
    Skill,
    SkillCategory,
    SocialLink,
)


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ('full_name', 'headline', 'available_for_work')
    fieldsets = (
        (None, {
            'fields': (
                'full_name', 'headline', 'tagline', 'about', 'location',
                'email', 'phone', 'show_phone', 'photo', 'resume_file',
                'available_for_work',
            ),
        }),
        ('English', {
            'classes': ('collapse',),
            'fields': (
                'full_name_en', 'headline_en', 'tagline_en', 'about_en', 'location_en',
            ),
        }),
    )


@admin.register(SocialLink)
class SocialLinkAdmin(ModelAdmin):
    list_display = ('label', 'url', 'order')
    list_editable = ('order',)


class SkillInline(TabularInline):
    model = Skill
    extra = 1


@admin.register(SkillCategory)
class SkillCategoryAdmin(ModelAdmin):
    list_display = ('name', 'name_en', 'order')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SkillInline]


@admin.register(Skill)
class SkillAdmin(ModelAdmin):
    list_display = ('name', 'name_en', 'category', 'level', 'featured', 'order')
    list_editable = ('level', 'featured', 'order')
    list_filter = ('category', 'featured')
    search_fields = ('name', 'name_en')


@admin.register(Experience)
class ExperienceAdmin(ModelAdmin):
    list_display = ('role', 'organization', 'period', 'is_current', 'order')
    list_editable = ('order',)
    list_filter = ('is_current',)
    fieldsets = (
        (None, {
            'fields': (
                'role', 'organization', 'location', 'period', 'start_date',
                'is_current', 'description', 'order',
            ),
        }),
        ('English', {
            'classes': ('collapse',),
            'fields': (
                'role_en', 'organization_en', 'location_en', 'period_en', 'description_en',
            ),
        }),
    )


@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = ('title', 'category', 'status', 'is_featured', 'is_private', 'order')
    list_editable = ('is_featured', 'order')
    list_filter = ('category', 'status', 'is_featured', 'is_private')
    search_fields = ('title', 'title_en', 'summary')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('skills',)
    fieldsets = (
        (None, {
            'fields': (
                'title', 'slug', 'summary', 'problem', 'solution', 'outcome',
                'category', 'status', 'skills', 'cover_image', 'github_url',
                'live_url', 'is_private', 'is_featured', 'order',
            ),
        }),
        ('English', {
            'classes': ('collapse',),
            'fields': (
                'title_en', 'summary_en', 'problem_en', 'solution_en', 'outcome_en',
            ),
        }),
    )


@admin.register(Certificate)
class CertificateAdmin(ModelAdmin):
    list_display = ('title', 'issuer', 'year', 'category', 'order')
    list_editable = ('order',)
    list_filter = ('category',)
    search_fields = ('title', 'title_en', 'issuer')
    fieldsets = (
        (None, {
            'fields': (
                'title', 'issuer', 'instructor', 'year', 'hours',
                'category', 'url', 'image', 'order',
            ),
        }),
        ('English', {
            'classes': ('collapse',),
            'fields': ('title_en', 'issuer_en', 'instructor_en', 'year_en'),
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_editable = ('is_read',)
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
