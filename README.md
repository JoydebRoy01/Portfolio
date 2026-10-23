# Portfolio site (Django)

A one-page professional portfolio with case-study pages, built with Django, plain HTML, CSS and JavaScript.

- Dark theme by default, with a light theme toggle in the header (remembered per visitor).
- Hero: a big brush-lettered name (Sedgwick Ave Display) behind a cut-out character; everything else uses Inter.
- A Three.js scene (`static/js/scene.js`) sits behind the page: embers, wireframe shapes and rings that the camera flies through as you scroll. Phones get a lighter version; visitors who turn off animations get a still frame.
- Sections tilt into view in 3D as you scroll (`static/js/site.js`).

The hero character is `static/img/hero-character.webp` (an alternative is `hero-character-alt.webp`). To use your own, upload a transparent PNG/WebP in Admin → Profile → Hero image. The original full-size AI images are in `design-assets/`.


## Run it locally

```bash
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_portfolio      # sample content so you can see the design
python manage.py createsuperuser     # your login for /admin
python manage.py runserver
```

Open http://127.0.0.1:8000 for the site and http://127.0.0.1:8000/admin to edit it.

## Make it yours

Everything on the page comes from the admin. You don't need to edit any templates.

| Admin section | What it controls |
|---|---|
| Profile | Name, role, headline, intro, availability, location, email, links, résumé PDF, photo, About text |
| Projects | Selected work list and each case-study page (problem, what you did, result, stack, links, screenshot) |
| Experience | Timeline of jobs. Leave the end date blank for your current role |
| Skill groups | Tool lists. Tick "Is primary" for the ones you use most weeks (shown in bold) |
| Messages | Everything sent through the contact form |

To reload the sample content from scratch: `python manage.py seed_portfolio --reset`.

## Contact form email

Messages are always saved under Admin → Messages. To also get an email, set `CONTACT_NOTIFY_EMAIL`, `DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`, and add your mail provider's `EMAIL_*` settings to `config/settings.py`.

## Deploying

Set these environment variables on the server:

- `DJANGO_SECRET_KEY`: a long random string
- `DJANGO_DEBUG=0`
- `DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com`
- `DJANGO_CSRF_TRUSTED_ORIGINS=https://yourdomain.com`

Then run `python manage.py collectstatic` and serve `staticfiles/` and `media/` from your web server.

## Tests

```bash
python manage.py test portfolio
```
