"""
View logic for cast management
"""

# Django
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
# This app
from .forms import AddManagerForm, CastForm, DeleteCastForm, PageSectionForm
from castpage.models import Cast, PageSection

@login_required
def cast_admin(request, slug: str):
    """
    Renders cast admin page
    """
    cast = get_object_or_404(Cast, slug=slug)
    if not cast.is_manager(request.user):
        return HttpResponseForbidden()
    return render(request, 'castadmin/admin.html', {'cast': cast})

@login_required
def cast_edit(request, slug: str):
    """
    Edit existing cast info
    """
    cast = get_object_or_404(Cast, slug=slug)
    if not cast.is_manager(request.user):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = CastForm(request.POST, request.FILES, instance=cast)
        if form.is_valid():
            cast = form.save()
            messages.success(request, 'Cast info has been updated')
            return redirect('cast_admin', slug=cast.slug)
    else:
        form = CastForm(instance=cast)
    return render(request, 'castadmin/cast_edit.html', {
        'cast': cast,
        'form': form,
        'tinymce_api_key': settings.TINYMCE_API_KEY,
    })

@login_required
def cast_delete(request, slug: str):
    """
    Delete a cast after verification
    """
    cast = get_object_or_404(Cast, slug=slug)
    if not cast.is_manager(request.user):
        return HttpResponseForbidden()
    if cast.managers.count() > 1:
        messages.info(request, 'Other managers must be removed before you can delete a cast')
        return redirect('cast_admin', slug=slug)
    if request.method == 'POST':
        form = DeleteCastForm(request.POST)
        if form.is_valid():
            castname = cast.name
            if form.cleaned_data.get('name') == castname:
                cast.delete()
                messages.success(request, f'You successfully deleted {castname}')
                return redirect('user_settings')
            else:
                messages.error(request, 'The cast name does not match')
    else:
        form = DeleteCastForm()
    return render(request, 'castadmin/delete.html', {
        'cast': cast,
        'form': form,
    })

@login_required
def section_new(request, slug: str):
    """
    Add a new PageSection to a cast's home page
    """
    cast = get_object_or_404(Cast, slug=slug)
    if not cast.is_manager(request.user):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = PageSectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.cast = cast
            section.save()
            return redirect('cast_home', slug=cast.slug)
    else:
        form = PageSectionForm()
    return render(request, 'castadmin/section_edit.html', {
        'cast': cast,
        'form': form,
        'tinymce_api_key': settings.TINYMCE_API_KEY,
    })

@login_required
def section_edit(request, slug: str, pk: int):
    """
    Edit an existing section of a cast's home page
    """
    cast = get_object_or_404(Cast, slug=slug)
    if not cast.is_manager(request.user):
        return HttpResponseForbidden()
    section = get_object_or_404(PageSection, pk=pk)
    if request.method == 'POST':
        form = PageSectionForm(request.POST, instance=section)
        if form.is_valid():
            section = form.save(commit=False)
            section.cast = cast
            section.save()
            return redirect('cast_home', slug=cast.slug)
    else:
        form = PageSectionForm(instance=section)
    return render(request, 'castadmin/section_edit.html', {
        'cast': cast,
        'form': form,
        'tinymce_api_key': settings.TINYMCE_API_KEY,
    })

@login_required
def section_delete(request, slug: str, pk: int):
    """
    Remove a section from a cast's home page
    """
    cast = get_object_or_404(Cast, slug=slug)
    if not cast.is_manager(request.user):
        return HttpResponseForbidden()
    section = get_object_or_404(PageSection, pk=pk)
    section.delete()
    return redirect('cast_home', slug=cast.slug)

@login_required
def managers_edit(request, slug: str):
    """
    Cast manager list and add page
    """
    cast = get_object_or_404(Cast, slug=slug)
    if not cast.is_manager(request.user):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = AddManagerForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username)
            if user:
                user = user[0]
                if cast.is_manager(user):
                    msg = f'{username} is already a manager'
                else:
                    cast.managers.add(user.profile)
                    msg = f'{user.first_name} {user.last_name} has been added as a manager'
                messages.error(request, msg)
            else:
                msg = f'Could not find an account for "{username}"'
                messages.error(request, msg)
            return redirect('cast_managers_edit', slug=cast.slug)
    else:
        form = AddManagerForm()
    return render(request, 'castadmin/managers.html', {
        'cast': cast,
        'form': form,
    })

@login_required
def managers_delete(request, slug: str, pk: int):
    """
    Remove a user from cast managers
    """
    cast = get_object_or_404(Cast, slug=slug)
    if not cast.is_manager(request.user):
        return HttpResponseForbidden()
    user = get_object_or_404(User, pk=pk)
    if cast.managers.count() < 2:
        messages.error(request, 'Casts must have at least one manager')
    elif request.user == user:
        messages.error(request, 'You cannot remove yourself')
    else:
        cast.managers.remove(user.profile)
        messages.success(request, f'{user.username} is no longer a manager')
    return redirect('cast_managers_edit', slug=cast.slug)
