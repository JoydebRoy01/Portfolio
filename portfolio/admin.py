from django.contrib import admin

from .models import (
    FAQ, ContactMessage, Experience, Principle, ProcessStep, Profile, Project, Service, Skill,
    SkillGroup, Testimonial,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Who you are", {"fields": ["name", "role", "photo", "hero_image"]}),
        ("Numbers at the top", {"fields": ["years_experience", "projects_built", "live_projects"]}),
        ("Top of the page", {"fields": ["headline", "intro"]}),
        ("Availability", {"fields": ["is_available", "availability_text", "location", "timezone_note"]}),
        ("Contact and links", {"fields": ["email", "phone", "github_url", "linkedin_url", "resume"]}),
        ("About section", {"fields": ["about"]}),
    ]

    def has_add_permission(self, request):
        return not Profile.objects.exists()


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "year", "kind", "is_featured", "order"]
    list_editable = ["is_featured", "order"]
    prepopulated_fields = {"slug": ["title"]}
    search_fields = ["title", "stack"]


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ["role", "company", "start_date", "end_date"]


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


@admin.register(SkillGroup)
class SkillGroupAdmin(admin.ModelAdmin):
    list_display = ["name", "order"]
    list_editable = ["order"]
    inlines = [SkillInline]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "reason", "created_at", "is_read"]
    list_filter = ["reason", "is_read"]
    list_editable = ["is_read"]
    readonly_fields = ["name", "email", "reason", "message", "created_at"]
    search_fields = ["name", "email", "message"]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["title", "stack", "order"]
    list_editable = ["order"]


@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ["title", "order"]
    list_editable = ["order"]


@admin.register(Principle)
class PrincipleAdmin(admin.ModelAdmin):
    list_display = ["title", "order"]
    list_editable = ["order"]


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ["name", "company", "is_published", "order"]
    list_editable = ["is_published", "order"]


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ["question", "order"]
    list_editable = ["order"]
