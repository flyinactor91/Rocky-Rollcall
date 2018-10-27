"""
View logic for calendar event management
"""

# stdlib
from datetime import date
# django
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.list import ListView
# app
from castpage.models import Cast
from .forms import EventForm
from .models import Event

@login_required
def event_new(request, slug: str):
    """
    Create a new event associated with a cast
    """
    cast = get_object_or_404(Cast, slug=slug)
    if not cast.is_manager(request.user):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.cast = cast
            event.save()
            messages.success(request, f'"{event.name}" has been created')
            if 'more' not in request.POST:
                return redirect('cast_events', slug=cast.slug)
    else:
        form = EventForm()
    return render(request, 'events/event_edit.html', {
        'form': form,
        'form_title': 'New Event',
        'show_ca_button': True,
    })

@login_required
def event_edit(request, pk: int):
    """
    Edit an existing event by primary key
    """
    event = get_object_or_404(Event, pk=pk)
    if not event.cast.is_manager(request.user):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'"{event.name}" has been updated')
            return redirect('cast_events', slug=event.cast.slug)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_edit.html', {
        'form': form,
        'form_title': 'Edit Event',
    })

@login_required
def event_delete(request, pk: int):
    """
    Delete an existing event by primary key
    """
    event = get_object_or_404(Event, pk=pk)
    if not event.cast.is_manager(request.user):
        return HttpResponseForbidden()
    event_name = event.name
    slug = event.cast.slug
    event.delete()
    messages.success(request, f'"{event_name}" has been deleted')
    return redirect('cast_home', slug=slug)

class EventListView(ListView):
    """
    Pagination view for future events
    """

    model = Event
    paginate_by = 12
    context_object_name = 'events'
    # pylint: disable=E1101
    queryset = Event.objects.filter(date__gte=date.today())

    def get_context_data(self, **kwargs) -> dict:
        """
        Return render context
        """
        context = super().get_context_data(**kwargs)
        context['show_cast'] = True
        return context