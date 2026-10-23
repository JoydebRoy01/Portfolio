from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from portfolio.models import ContactMessage, Project, Testimonial


class EmptySiteTests(TestCase):
    def test_home_without_profile_shows_setup_prompt(self):
        res = self.client.get(reverse("portfolio:home"))
        self.assertContains(res, "Your portfolio has no content yet")


class SeededSiteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_portfolio", verbosity=0)

    def test_home_renders_all_sections(self):
        res = self.client.get(reverse("portfolio:home"))
        self.assertEqual(res.status_code, 200)
        for anchor in ['id="work"', 'id="experience"', 'id="about"', 'id="contact"']:
            self.assertContains(res, anchor)
        self.assertContains(res, "Himalayan Hives")

    def test_hero_stats_use_profile_numbers(self):
        res = self.client.get(reverse("portfolio:home"))
        self.assertContains(res, "<dd>2+</dd>", html=False)
        self.assertContains(res, "<dd>50+</dd>", html=False)
        self.assertContains(res, "<dd>10+</dd>", html=False)
        self.assertContains(res, "Websites &amp; web apps")

    def test_experience_shows_years_only(self):
        res = self.client.get(reverse("portfolio:home"))
        html = res.content.decode()
        self.assertIn("Associate software engineer", html)
        self.assertIn("Corunit", html)
        self.assertIn('<time datetime="2024">2024</time>', html)
        self.assertNotIn("Jan 2024", html)
        self.assertNotIn("Northwind", html)

    def test_more_projects_and_live_links(self):
        res = self.client.get(reverse("portfolio:home"))
        self.assertContains(res, "More projects")
        self.assertContains(res, "Food Delivery Web App")
        self.assertContains(res, 'href="https://darjeelingtrips.com/"')
        self.assertContains(res, "Visit darjeelingtrips.com")

    def test_project_page_hides_empty_sections(self):
        res = self.client.get(reverse("portfolio:project_detail", args=["hrms"]))
        self.assertContains(res, "HRMS")
        self.assertNotContains(res, "The problem")
        self.assertNotContains(res, "<h2>Result</h2>", html=False)

    def test_home_renders_new_sections_and_footer(self):
        res = self.client.get(reverse("portfolio:home"))
        for anchor in ['id="services"', 'id="process"', 'id="principles"', 'id="faq"', 'class="cta"', 'class="site-footer"']:
            self.assertContains(res, anchor)
        self.assertContains(res, "Django backends &amp; APIs")

    def test_testimonials_hidden_until_added(self):
        res = self.client.get(reverse("portfolio:home"))
        self.assertNotContains(res, 'id="testimonials"')
        Testimonial.objects.create(quote="Joydeb shipped our booking flow early.", name="Sam Lee", company="Acme")
        res = self.client.get(reverse("portfolio:home"))
        self.assertContains(res, 'id="testimonials"')
        self.assertContains(res, "Sam Lee")

    def test_footer_on_case_study_lists_services(self):
        res = self.client.get(Project.objects.first().get_absolute_url())
        self.assertContains(res, 'class="site-footer"')
        self.assertContains(res, "AWS deployment &amp; CI/CD")

    def test_project_detail(self):
        project = Project.objects.first()
        res = self.client.get(project.get_absolute_url())
        self.assertContains(res, project.outcome)
        self.assertContains(res, "Next project")

    def test_unknown_project_is_404(self):
        res = self.client.get("/work/does-not-exist/")
        self.assertEqual(res.status_code, 404)

    def test_contact_fetch_success_saves_message(self):
        res = self.client.post(
            reverse("portfolio:contact"),
            {"name": "Sam", "email": "sam@example.com", "reason": "job",
             "message": "We have a senior Django role open."},
            HTTP_X_REQUESTED_WITH="fetch",
        )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json()["ok"])
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_contact_fetch_errors(self):
        res = self.client.post(
            reverse("portfolio:contact"),
            {"name": "", "email": "nope", "reason": "job", "message": "hi"},
            HTTP_X_REQUESTED_WITH="fetch",
        )
        self.assertEqual(res.status_code, 400)
        self.assertEqual(set(res.json()["errors"]), {"name", "email", "message"})

    def test_contact_honeypot_is_not_saved(self):
        self.client.post(
            reverse("portfolio:contact"),
            {"name": "Bot", "email": "bot@example.com", "reason": "job",
             "message": "Buy cheap things now please", "website": "spam.example"},
        )
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_contact_without_js_redirects_with_message(self):
        res = self.client.post(
            reverse("portfolio:contact"),
            {"name": "Sam", "email": "sam@example.com", "reason": "project",
             "message": "Could you help with a small app?"},
            follow=True,
        )
        self.assertContains(res, "Message sent")


class ToolIconTests(TestCase):
    def test_icon_is_picked_from_name_or_admin_choice(self):
        from portfolio.models import Skill, SkillGroup
        group = SkillGroup.objects.create(name="Back end")
        self.assertEqual(Skill(group=group, name="PostgreSQL").icon_slug, "postgresql")
        self.assertEqual(Skill(group=group, name="Django REST Framework").icon_slug, "django")
        self.assertEqual(Skill(group=group, name="Something new").icon_slug, "default")
        self.assertEqual(Skill(group=group, name="Something new", icon="docker").icon_slug, "docker")
