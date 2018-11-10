"""
Castpage URL patterns
"""

from django.urls import path
from castpage import views

urlpatterns = [
    path('new', views.cast_new, name='cast_new'),
    path('<slug:slug>', views.cast_home, name='cast_home'),
    path('<slug:slug>/events', views.CastEvents.as_view(), name='cast_events'),
    path('<slug:slug>/photos', views.CastPhotos.as_view(), name='cast_photos'),
    path('<slug:slug>/photos/<int:pk>', views.cast_photo_detail, name='cast_photo_detail'),
]
