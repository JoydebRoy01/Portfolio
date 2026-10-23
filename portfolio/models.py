from django.db import models
from django.urls import reverse

from .tool_icons import ICON_CHOICES, icon_for


class Profile(models.Model):
    """The person the site is about. Only the first row is used."""

    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120, help_text="e.g. Full-stack developer")
    headline = models.CharField(
        max_length=200,
        help_text="One sentence on what you do and for whom. Shown large at the top.",
    )
    intro = models.TextField(help_text="Two or three sentences under the headline.")
    about = models.TextField(help_text="Longer bio for the About section. Blank lines start new paragraphs.")
    location = models.CharField(max_length=120)
    timezone_note = models.CharField(max_length=120, blank=True, help_text="e.g. IST, works with EU and US teams")
    is_available = models.BooleanField(default=True, help_text="Shows the green availability marker.")
    availability_text = models.CharField(
        max_length=160,
        default="Open to full-time roles and freelance projects",
    )
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    resume = models.FileField(upload_to="resume/", blank=True)
    photo = models.ImageField(upload_to="profile/", blank=True)
    hero_image = models.ImageField(
        upload_to="profile/", blank=True,
        help_text="Cut-out figure (transparent PNG/WebP) shown in front of your name at the top. "
                  "Leave blank to use the built-in character.",
    )
    years_experience = models.PositiveSmallIntegerField(default=0)
    projects_built = models.PositiveSmallIntegerField(
        null=True, blank=True,
        help_text="Total websites and web apps you've built (shown as e.g. 50+). Leave blank to count the projects added here.",
    )
    live_projects = models.PositiveSmallIntegerField(
        null=True, blank=True,
        help_text="How many are live right now (shown as e.g. 10+). Leave blank to count projects with a live link.",
    )

    class Meta:
        verbose_name = "profile"

    def __str__(self):
        return self.name

    @property
    def first_name(self):
        return self.name.split(" ")[0]

    @property
    def last_name(self):
        return " ".join(self.name.split(" ")[1:])

    @property
    def hero_chars(self):
        """Length of the longer name line, used to size the hero lettering so it fits."""
        return max(len(self.first_name), len(self.last_name), 3)

    @property
    def initials(self):
        return "".join(part[0] for part in self.name.split()[:2]).upper()

    def about_paragraphs(self):
        return [p.strip() for p in self.about.split("\n\n") if p.strip()]


class Project(models.Model):
    TONE_CHOICES = [
        ("cobalt", "Cobalt"),
        ("pine", "Pine"),
        ("plum", "Plum"),
        ("slate", "Slate"),
    ]

    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    kind = models.CharField(max_length=80, help_text="e.g. Client project, Product, Open source")
    summary = models.CharField(max_length=220, help_text="One line shown in the list.")
    my_role = models.CharField(max_length=160, blank=True)
    problem = models.TextField(blank=True, help_text="What was wrong or missing before.")
    approach = models.TextField(blank=True, help_text="What you did. Blank lines start new paragraphs.")
    outcome = models.CharField(max_length=200, blank=True, help_text="The measurable result, one line. Leave blank if you don't have a number yet.")
    stack = models.CharField(max_length=240, blank=True, help_text="Comma-separated, e.g. Django, PostgreSQL, Redis")
    image = models.ImageField(upload_to="projects/", blank=True)
    tone = models.CharField(max_length=10, choices=TONE_CHOICES, default="cobalt",
                            help_text="Panel colour used when there is no image.")
    live_url = models.URLField(blank=True)
    repo_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=True, help_text="Featured projects get the big list; the rest appear under More projects.")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "-year", "title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("portfolio:project_detail", args=[self.slug])

    @property
    def live_domain(self):
        """e.g. "darjeelingtrips.com" from the live URL, for link text."""
        if not self.live_url:
            return ""
        host = self.live_url.split("//", 1)[-1].split("/", 1)[0]
        return host.removeprefix("www.")

    def stack_list(self):
        return [s.strip() for s in self.stack.split(",") if s.strip()]

    def approach_paragraphs(self):
        return [p.strip() for p in self.approach.split("\n\n") if p.strip()]


class Experience(models.Model):
    company = models.CharField(max_length=120, blank=True)
    company_url = models.URLField(blank=True)
    role = models.CharField(max_length=120)
    location = models.CharField(max_length=120, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text="Leave blank if this is your current job.")
    year_only = models.BooleanField(
        default=False,
        help_text="Show only the years (e.g. 2024 to 2025) when you don't want to show months.",
    )
    summary = models.CharField(max_length=240, blank=True)
    highlights = models.TextField(blank=True, help_text="One achievement per line.")

    class Meta:
        ordering = ["-start_date"]
        verbose_name_plural = "experience"

    def __str__(self):
        return f"{self.role} at {self.company}" if self.company else self.role

    @property
    def is_current(self):
        return self.end_date is None

    def highlight_list(self):
        return [h.strip() for h in self.highlights.splitlines() if h.strip()]


class SkillGroup(models.Model):
    name = models.CharField(max_length=80)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class Skill(models.Model):
    group = models.ForeignKey(SkillGroup, related_name="skills", on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    is_primary = models.BooleanField(default=False, help_text="Daily-use skills get a \"Daily\" badge.")
    icon = models.CharField(
        max_length=40, blank=True, choices=ICON_CHOICES,
        help_text="Leave blank to pick the icon automatically from the name.",
    )
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    @property
    def icon_slug(self):
        return icon_for(self.name, self.icon)[0]

    @property
    def brand_color(self):
        return icon_for(self.name, self.icon)[1] or ""


class ContactMessage(models.Model):
    REASON_CHOICES = [
        ("job", "A job opening"),
        ("project", "A freelance project"),
        ("other", "Something else"),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField()
    reason = models.CharField(max_length=10, choices=REASON_CHOICES, default="job")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "message"

    def __str__(self):
        return f"{self.name} — {self.get_reason_display()}"


class Service(models.Model):
    title = models.CharField(max_length=100)
    summary = models.CharField(max_length=220)
    stack = models.CharField(max_length=160, blank=True, help_text="Comma-separated, e.g. Django, PostgreSQL")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title

    def stack_list(self):
        return [s.strip() for s in self.stack.split(",") if s.strip()]


class ProcessStep(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "process step"

    def __str__(self):
        return self.title


class Principle(models.Model):
    title = models.CharField(max_length=100, help_text="A short statement, e.g. Keep the stack boring.")
    description = models.CharField(max_length=220)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    quote = models.TextField(help_text="Use the person's real words, with their permission.")
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120, blank=True)
    company = models.CharField(max_length=120, blank=True)
    is_published = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.name}{', ' + self.company if self.company else ''}"

    @property
    def initials(self):
        return "".join(part[0] for part in self.name.split()[:2]).upper()


class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question
