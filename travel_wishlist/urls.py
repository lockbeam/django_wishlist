from django.urls import path
from . import views
# path describes what a url looks like

# below are lists of urls or app will recognize
urlpatterns = [
    path('', views.place_list, name ='place_list'),
    path('visited', views.places_visited, name='places_visited'),
    path('place/<int:place_pk>/was_visited', views.place_was_visited, name='place_was_visited'),
    path('place/<int:place_pk>', views.place_details, name='place_details'), #will create url based on primary key of location
    path('place/<int:place_pk>/delete', views.delete_place, name='delete_place')
]

