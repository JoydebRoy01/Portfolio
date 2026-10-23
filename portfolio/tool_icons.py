"""Icons for the "Tools I use" list.

Each icon is an SVG in static/img/tools/<slug>.svg (brand logos from Simple Icons,
plus a few hand-drawn generic ones). A skill gets its icon automatically from its
name, or you can pick one in the admin.
"""

# slug: (label for the admin, brand colour or None to use the accent colour)
ICONS = {
    "python": ("Python", "#3776AB"),
    "django": ("Django", "#44B78B"),
    "postgresql": ("PostgreSQL", "#4169E1"),
    "sqlite": ("SQLite", "#0F80CC"),
    "cpanel": ("cPanel", "#FF6C2C"),
    "celery": ("Celery", "#37814A"),
    "redis": ("Redis", "#FF4438"),
    "javascript": ("JavaScript", "#F7DF1E"),
    "html5": ("HTML", "#E34F26"),
    "css3": ("CSS", "#1572B6"),
    "htmx": ("htmx", "#3366CC"),
    "react": ("React", "#61DAFB"),
    "docker": ("Docker", "#2496ED"),
    "githubactions": ("GitHub Actions", "#2088FF"),
    "github": ("GitHub", None),
    "git": ("Git", "#F05032"),
    "amazonwebservices": ("AWS", "#FF9900"),
    "nginx": ("Nginx", "#009639"),
    "sentry": ("Sentry", "#8A72C7"),
    "fastapi": ("FastAPI", "#009688"),
    "linux": ("Linux", "#FCC624"),
    "nodedotjs": ("Node.js", "#5FA04E"),
    "ollama": ("Ollama", None),
    "langchain": ("LangChain / LangGraph", None),
    "accessibility": ("Accessibility", None),
    "code-review": ("Code review", None),
    "writing": ("Writing / docs", None),
    "mentoring": ("Mentoring / people", None),
    "interviews": ("Interviews / chat", None),
    "default": ("Generic code", None),
}

ICON_CHOICES = [(slug, label) for slug, (label, _) in ICONS.items()]

# First match wins, so more specific names come first.
_KEYWORDS = [
    ("django rest", "django"),
    ("django", "django"),
    ("python", "python"),
    ("postgres", "postgresql"),
    ("sqlite", "sqlite"),
    ("cpanel", "cpanel"),
    ("celery", "celery"),
    ("redis", "redis"),
    ("javascript", "javascript"),
    ("html", "html5"),
    ("css", "css3"),
    ("htmx", "htmx"),
    ("react", "react"),
    ("docker", "docker"),
    ("github actions", "githubactions"),
    ("github", "github"),
    ("git", "git"),
    ("aws", "amazonwebservices"),
    ("amazon", "amazonwebservices"),
    ("ec2", "amazonwebservices"),
    ("nginx", "nginx"),
    ("sentry", "sentry"),
    ("fastapi", "fastapi"),
    ("linux", "linux"),
    ("node", "nodedotjs"),
    ("ollama", "ollama"),
    ("langchain", "langchain"),
    ("langgraph", "langchain"),
    ("accessib", "accessibility"),
    ("review", "code-review"),
    ("spec", "writing"),
    ("writing", "writing"),
    ("docs", "writing"),
    ("mentor", "mentoring"),
    ("teach", "mentoring"),
    ("interview", "interviews"),
    ("research", "interviews"),
]


def icon_for(name, chosen=""):
    """Return (slug, brand colour or None) for a skill."""
    if chosen in ICONS:
        return chosen, ICONS[chosen][1]
    lowered = name.lower()
    for keyword, slug in _KEYWORDS:
        if keyword in lowered:
            # Django REST Framework gets DRF's red so it differs from plain Django
            if keyword == "django rest":
                return slug, "#E0474C"
            return slug, ICONS[slug][1]
    return "default", None
