from django.shortcuts import render
from castpage.models import Cast
from events.models import get_upcoming_events

def home(request):
    """
    Renders the landing page
    """
    return render(request, 'landingpage/landingpage.html', {
        'casts': Cast.objects.all(),
        'calendar': get_upcoming_events(),
        'show_cast': True,
    })
