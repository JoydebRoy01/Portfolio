from .models import Profile, Service


def site_profile(request):
    # Services are shown on the home page and listed in the footer of every page.
    return {
        "profile": Profile.objects.first(),
        "services": Service.objects.all(),
    }
