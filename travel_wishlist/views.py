from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm

# Create your views here.

def place_list(request):

    if request.method == 'POST':
        # create a new place but from data on the page
        # if data is valid save and basically refresh page
        form = NewPlaceForm(request.POST)
        place = form.save() # creating a model object from form
        if form.is_valid(): # validation against database contraints
            place.save() # saves place to database
            return redirect('place_list') # reloads home page with url place_list

    #before displaying results actually query the database
    # below would be get everything
    # places = Place.objects.all()
    # however we want to prefilter and only display places NOT visited
    places = Place.objects.filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()
    # return render of request with template
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})

def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', { "visited": visited })

def place_was_visited(request, place_pk):
    if request.method == 'POST':
        # below is database query that gets the value for the place_pk (primary key identifier)
        # place = Place.objects.get(pk=place_pk)
        # replaced with below to handle requesting changes to a city or pk that doesn't exist
        place = get_object_or_404(Place, pk=place_pk)
        place.visited = True # update visited value to True
        place.save() # and save to database

    return redirect('places_visited') #redirect to places visited
    # return redirect('place_list') # redirect (basically refresh) to wishlist places

def about(request):
    author = 'Devin'
    about = "A website to create a list of places to visit"
    # need to create new template for this
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})
