"""Fill the site with sample content so you can see the design.

Run:  python manage.py seed_portfolio
Then replace everything in /admin with your own details.
Use --reset to wipe existing portfolio content first.
"""

from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction

from portfolio.models import (
    FAQ, Experience, Principle, ProcessStep, Profile, Project, Service, Skill, SkillGroup,
)

PROFILE = dict(
    name="Joydeb Roy",
    role="Full-stack developer",
    headline="I build web products that stay fast and easy to change as they grow.",
    intro=(
        "I work across Django back ends and JavaScript front ends, from the database "
        "schema to the last pixel. Most recently I led the rebuild of a billing "
        "platform used by 140 agencies."
    ),
    about=(
        "I started writing code to automate spreadsheets at my first job in operations. "
        "Today I still care most about the same thing: software that removes "
        "tedious work for the people who use it every day.\n\n"
        "My usual role is the developer who owns a feature end to end. I talk to the "
        "people who will use it, design the data model, write the API and the interface, "
        "and stay around after launch to measure whether it worked.\n\n"
        "Outside work I maintain a small open-source logging library and mentor first-time "
        "contributors at local Django meetups."
    ),
    location="West Bengal, India",
    timezone_note="IST, overlaps with EU mornings and US evenings",
    is_available=True,
    availability_text="Open to full-time roles and freelance projects",
    email="hello@example.com",
    github_url="https://github.com/JoydebRoy01",
    linkedin_url="https://www.linkedin.com/in/joydeb-roy-351939324/",
    years_experience=2,
    projects_built=50,
    live_projects=10,
)

# Joydeb's real projects. Only facts he has given are filled in; the rest
# (year, role, results) is left blank to complete in the admin.
PROJECTS = [
    # Main projects: shown in the big "Selected work" list
    dict(
        title="PRM", slug="prm", kind="Live web system", tone="cobalt",
        summary="A live system built for A One Health Wellness.",
        stack="Python, Django, PostgreSQL, SQLite, cPanel",
        live_url="https://system.aonehealthwellness.com/", order=1,
    ),
    dict(
        title="Himalayan Hives", slug="himalayan-hives", kind="Travel & tour booking", tone="pine",
        summary="Travel and tour booking website with destination pages and tour listings.",
        stack="Python, Django, PostgreSQL, SQLite, cPanel, HTML, CSS, Bootstrap, JavaScript, Leaflet.js",
        approach="I worked on the destination pages, tour listings, banners and the dynamic content that's managed from the admin.", order=2,
    ),
    dict(
        title="Team Platform", slug="team-platform", kind="Collaboration & project management", tone="plum",
        summary="A platform for teams to manage projects, tasks and communication in one place.",
        stack="Python, Django, Django REST Framework, PostgreSQL, SQLite, cPanel",
        approach="It's built as separate modules: accounts, projects, tasks, communication, Git integration, analytics and notifications.", order=3,
    ),
    dict(
        title="Expense Tracker", slug="expense-tracker", kind="Mobile app", tone="slate",
        summary="Mobile app for managing expenses.",
        stack="Ionic, Angular, TypeScript, Capacitor, Django, PostgreSQL, SQLite, cPanel",
        approach="I worked on the mobile app development and its Android deployment.", order=4,
    ),
    # Other projects: shown as smaller cards under "More projects"
    dict(
        title="Darjeeling Trips", slug="darjeeling-trips", kind="Travel website", tone="pine",
        summary="Tour website for Darjeeling, with fully automated deployment.",
        stack="Python, Django, PostgreSQL, SQLite, cPanel, AWS EC2, GitHub Actions",
        live_url="https://darjeelingtrips.com/", is_featured=False, order=10,
    ),
    dict(
        title="Food Delivery Web App", slug="food-delivery", kind="Web app", tone="cobalt",
        summary="Food ordering and delivery platform for Pokhara, Kathmandu and Chitwan in Nepal.",
        stack="Python, Django, PostgreSQL, SQLite, cPanel",
        is_featured=False, order=11,
    ),
    dict(
        title="HRMS", slug="hrms", kind="Employee management system", tone="slate",
        summary="Employee management and day-to-day HR operations.",
        stack="Python, Django, PostgreSQL, SQLite, cPanel",
        is_featured=False, order=12,
    ),
    dict(
        title="ATS", slug="ats", kind="Applicant tracking system", tone="plum",
        summary="Resume parsing, candidate tracking, interview scheduling and offer letters.",
        stack="Python, Django, PostgreSQL, SQLite, cPanel",
        is_featured=False, order=13,
    ),
    dict(
        title="Billing, EMR & Invoices", slug="billing-emr", kind="Healthcare system", tone="pine",
        summary="Billing, invoices and medical-record workflows.",
        stack="Python, Django, PostgreSQL, SQLite, cPanel",
        is_featured=False, order=14,
    ),
    dict(
        title="Developer Portfolio", slug="developer-portfolio", kind="Personal website", tone="cobalt",
        summary="This site: my portfolio for freelance work and job opportunities.",
        stack="Python, Django, SQLite, JavaScript, Three.js",
        is_featured=False, order=15,
    ),
]

# Joydeb's real roles. Months aren't known yet, so only years are shown.
EXPERIENCE = [
    dict(
        role="Full-stack developer", company="", location="West Bengal, India",
        start_date=date(2026, 1, 1), end_date=None, year_only=True,
    ),
    dict(
        role="Associate software engineer", company="Corunit",
        start_date=date(2025, 1, 1), end_date=date(2026, 1, 1), year_only=True,
    ),
    dict(
        role="Software engineering intern", company="",
        start_date=date(2024, 1, 1), end_date=date(2024, 12, 31), year_only=True,
    ),
]

SKILLS = {
    "Back end": [("Python", True), ("Django", True), ("Django REST Framework", True),
                 ("PostgreSQL", True), ("SQLite", True), ("Celery", False), ("Redis", False)],
    "Front end": [("JavaScript", True), ("HTML and CSS", True), ("HTMX", False),
                  ("React", False), ("Accessibility", False)],
    "Infrastructure": [("cPanel", True), ("Docker", True), ("GitHub Actions", False), ("AWS", False),
                       ("Nginx", False), ("Sentry", False)],
    "Ways of working": [("Code review", True), ("Writing specs", False),
                        ("Mentoring", False), ("User interviews", False)],
}


# Services, process, principles and FAQ come from Joydeb's earlier site.
SERVICES = [
    ("Django backends & APIs", "Multi-user applications with roles and OTP-based onboarding.", "Django, PostgreSQL"),
    ("AWS deployment & CI/CD", "EC2, RDS, and S3 with Nginx, Gunicorn, SSL, and automated deployments.", "AWS, GitHub Actions"),
    ("Frontend dashboards", "Clear data views and dashboards designed around real users.", "HTML, CSS, JavaScript"),
    ("AI agent prototypes", "Self-hosted agent loops that plan, work, and review.", "Ollama, LangGraph, FastAPI"),
]

PROCESS = [
    ("Understand", "Map the whole flow with the people who will use it. Start with how a customer places an order and how the shop owner receives it."),
    ("Design", "Define roles, models, and APIs: who can do what, and how users get in. The booking system uses OTP-based onboarding."),
    ("Build", "Build the Django application on PostgreSQL, with clear frontend views and dashboards where people need them."),
    ("Deploy", "Set up Nginx, Gunicorn, and SSL on AWS. GitHub Actions can handle rsync, migrations, static files, and service restarts."),
    ("Monitor", "Watch application health, logs, and user feedback after launch so issues are easy to spot."),
    ("Improve", "Use what the live system teaches us to refine the experience and make the next release more useful."),
]

PRINCIPLES = [
    ("Automate the boring parts.", "Deploys, migrations, and static files should run themselves."),
    ("Keep the stack boring.", "Django, PostgreSQL, Nginx, and Gunicorn: proven tools, fewer surprises."),
    ("Secure by default.", "OTP-based sign-up and SSL belong in the first build, not as an afterthought."),
    ("Build for the person using it.", "Dashboards and order flows should make sense on day one."),
    ("Make failures visible.", "Useful logs and clear error states make problems easier to find and fix."),
    ("Ship in small steps.", "Frequent, focused releases make it easier to learn, improve, and roll back safely."),
]

FAQS = [
    ("What do you mainly work with?", "Python and Django, with FastAPI or Node.js when they fit better, on PostgreSQL and AWS."),
    ("Can you handle deployment too?", "Yes. I set up EC2, RDS, and S3 with Nginx, Gunicorn, and SSL, and automate deployments with GitHub Actions."),
    ("Are you available for projects?", "Availability depends on the scope and timing. Send me a brief and timeline, and I'll let you know whether I can take it on."),
    ("Do you build with AI?", "Yes. I build self-hosted agent systems with Ollama, LangGraph, and FastAPI, and explore multi-agent patterns with CrewAI and AutoGen."),
]


def seed_sections(stdout):
    """Fill the Services, Process, Principles and FAQ sections if they're empty."""
    filled = []
    if not Service.objects.exists():
        for i, (title, summary, stack) in enumerate(SERVICES):
            Service.objects.create(title=title, summary=summary, stack=stack, order=i)
        filled.append("services")
    if not ProcessStep.objects.exists():
        for i, (title, desc) in enumerate(PROCESS):
            ProcessStep.objects.create(title=title, description=desc, order=i)
        filled.append("process")
    if not Principle.objects.exists():
        for i, (title, desc) in enumerate(PRINCIPLES):
            Principle.objects.create(title=title, description=desc, order=i)
        filled.append("principles")
    if not FAQ.objects.exists():
        for i, (q, a) in enumerate(FAQS):
            FAQ.objects.create(question=q, answer=a, order=i)
        filled.append("FAQ")
    if filled:
        stdout.write("Added " + ", ".join(filled) + ".")


class Command(BaseCommand):
    help = "Load sample portfolio content. Replace it with your own in /admin."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Delete existing portfolio content first.")

    @transaction.atomic
    def handle(self, *args, reset=False, **options):
        if reset:
            for model in (Skill, SkillGroup, Experience, Project, Profile, Service, ProcessStep, Principle, FAQ):
                model.objects.all().delete()
        elif Profile.objects.exists():
            seed_sections(self.stdout)
            self.stdout.write(self.style.WARNING(
                "Profile content already exists, so it was left as is. Use --reset to replace everything."
            ))
            return

        Profile.objects.create(**PROFILE)
        for p in PROJECTS:
            Project.objects.create(**p)
        for e in EXPERIENCE:
            Experience.objects.create(**e)
        for i, (group_name, skills) in enumerate(SKILLS.items()):
            group = SkillGroup.objects.create(name=group_name, order=i)
            for j, (name, primary) in enumerate(skills):
                Skill.objects.create(group=group, name=name, is_primary=primary, order=j)

        seed_sections(self.stdout)
        self.stdout.write(self.style.SUCCESS("Sample content loaded. Edit it at /admin."))
