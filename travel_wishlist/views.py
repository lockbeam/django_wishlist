from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

# Create your views here.

@login_required
def place_list(request):

    if request.method == 'POST':
        # create a new place but from data on the page
        # if data is valid save and basically refresh page
        form = NewPlaceForm(request.POST)
        place = form.save(commit=False) # creating a model object from form
        place.user = request.user
        if form.is_valid(): # validation against database contraints
            place.save() # saves place to database
            return redirect('place_list') # reloads home page with url place_list

    #before displaying results actually query the database
    # below would be get everything
    # places = Place.objects.all()
    # however we want to prefilter and only display places NOT visited
    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()
    # return render of request with template
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})

@login_required
def places_visited(request):
    visited = Place.objects.filter(user=request.user).filter(visited=True).order_by('name')
    return render(request, 'travel_wishlist/visited.html', { "visited": visited })

@login_required
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        # below is database query that gets the value for the place_pk (primary key identifier)
        # place = Place.objects.get(pk=place_pk)
        # replaced with below to handle requesting changes to a city or pk that doesn't exist
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == request.user: #user can only visit their own places
            place.visited = True # update visited value to True
            place.save() # and save to database
        else:
            return HttpResponseForbidden()

    return redirect('places_visited') #redirect to places visited
    # return redirect('place_list') # redirect (basically refresh) to wishlist places

@login_required
def place_details(request, place_pk):
        place = get_object_or_404(Place, pk=place_pk)
        # does this place belong to the current user?
        if place.user != request.user:
            return HttpResponseForbidden()
        # is this a GET or a POST request?
        if request.method == 'POST':
            # create a new form with the new object data
            form = TripReviewForm(request.POST, request.FILES, instance=place)
            # are all the required inputs completed and if so are they also valid?
            if form.is_valid():
            # add and save, confirm visually
                form.save()
                messages.info(request, 'Trip information updated!')
            else:
                messages.error(request, form.errors) # TODO temporary
            
            return redirect('place_details', place_pk=place_pk)
        
        # GET - show place info and form
        # if not visited,, no form should show
        else:
            if place.visited:
                review_form = TripReviewForm(instance=place)
                return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form} )
            else:
                return render(request, 'travel_wishlist/place_detail.html', {'place': place} )


@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list') # so web page doesn't time out
    else:
        return HttpResponseForbidden()

