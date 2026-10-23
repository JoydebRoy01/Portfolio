import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ContactForm
from .models import FAQ, Experience, Principle, ProcessStep, Project, Skill, SkillGroup, Testimonial

logger = logging.getLogger(__name__)

SUCCESS_TEXT = "Thanks for writing. I reply to most messages within two working days."


def _home_context(form):
    return {
        "projects": Project.objects.filter(is_featured=True),
        "other_projects": Project.objects.filter(is_featured=False),
        "project_count": Project.objects.count(),
        "live_count": Project.objects.exclude(live_url="").count(),
        "experience": Experience.objects.all(),
        "skill_groups": SkillGroup.objects.prefetch_related("skills"),
        "marquee_skills": Skill.objects.order_by("group__order", "order"),
        "process_steps": ProcessStep.objects.all(),
        "principles": Principle.objects.all(),
        "testimonials": Testimonial.objects.filter(is_published=True),
        "faqs": FAQ.objects.all(),
        "form": form,
    }


def home(request):
    return render(request, "portfolio/home.html", _home_context(ContactForm()))


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    projects = list(Project.objects.filter(is_featured=True))
    next_project = None
    if project in projects and len(projects) > 1:
        next_project = projects[(projects.index(project) + 1) % len(projects)]
    return render(request, "portfolio/project_detail.html", {
        "project": project,
        "next_project": next_project,
    })


def _wants_json(request):
    return request.headers.get("x-requested-with") == "fetch"


@require_POST
def contact(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        if not form.is_spam():
            msg = form.save()
            _notify(msg)
        if _wants_json(request):
            return JsonResponse({"ok": True, "message": SUCCESS_TEXT})
        messages.success(request, SUCCESS_TEXT)
        return redirect("/#contact")

    if _wants_json(request):
        errors = {field: [str(e) for e in errs] for field, errs in form.errors.items()}
        return JsonResponse({"ok": False, "errors": errors}, status=400)

    return render(request, "portfolio/home.html", _home_context(form), status=400)


def _notify(msg):
    if not settings.CONTACT_NOTIFY_EMAIL:
        return
    try:
        send_mail(
            subject=f"Portfolio: {msg.get_reason_display()} from {msg.name}",
            message=f"{msg.message}\n\nReply to: {msg.email}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_NOTIFY_EMAIL],
        )
    except Exception:  # The message is already saved; email is a bonus.
        logger.exception("Could not send contact notification")


def not_found(request, exception):
    return render(request, "404.html", status=404)
