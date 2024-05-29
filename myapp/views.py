from django.shortcuts import render, redirect, get_object_or_404
from .forms import DestinationForm, ReviewForm, RegistrationForm, ProfileEditForm, PasswordUpdateForm, SearchForm
from myapp.models import Place, Destination, Review, SearchHistory
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.utils import timezone
from django.db import models
from datetime import timedelta






def home(request):
    recent_places = Destination.objects.all().order_by('-id')[:5]
    popular_places = Destination.objects.all().order_by('-popularity_count')[:6]
    return render(request, 'welcome.html', context={
        'recent_places': recent_places,
        'popular_places': popular_places
    })


def add_place(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to home or another appropriate page
    else:
        form = DestinationForm()
    return render(request, 'add_place.html', {'form': form})


def place_detail(request, place_id):
    place = get_object_or_404(Destination, pk=place_id)
    reviews = Review.objects.filter(place=place)

    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(place=place, user=request.user).first()

        if request.method == 'POST':
            if user_review:
                form = ReviewForm(request.POST, request.FILES, instance=user_review)
            else:
                form = ReviewForm(request.POST, request.FILES)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.place = place
                review.save()
                return redirect('place_detail', place_id=place.id)
        else:
            if user_review:
                form = ReviewForm(instance=user_review)
            else:
                form = ReviewForm()
    else:
        form = None

    context = {
        'place': place,
        'reviews': reviews,
        'form': form,
        'user_review': user_review,
    }
    return render(request, 'place_detail.html', context)

@login_required
def add_review(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.place = destination
            review.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('place_detail', place_id=destination.pk)
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form, 'destination': destination})


def destination_list(request):
    destinations = Destination.objects.all()
    return render(request, 'destination_list.html', {'destinations': destinations})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            return redirect('login')  # Redirect to login page or another page
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    # Fetch the necessary information
    user = request.user
    user_reviews = Review.objects.filter(user=user).order_by('-created_at')

    context = {
        'username': user.username,
        'joined_date': user.date_joined.strftime("%B %d, %Y"),
        'reviews': user_reviews,
        # Add other information as needed
    }

    return render(request, 'profile.html', context)

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, ('You were logged out successfully'))
    return redirect('home')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        password_form = PasswordUpdateForm(request.user, request.POST)

        if form.is_valid():
            form.save()  # Save changes to user information
            messages.success(request, 'Profile updated successfully!')
        if password_form.is_valid():
            password_form.save()  # Save password change
            update_session_auth_hash(request, password_form.user)  # Prevents logout
            messages.success(request, 'Password updated successfully!')

        return redirect('profile')  # Redirect back to profile page

    else:
        form = ProfileEditForm(instance=request.user)
        password_form = PasswordUpdateForm(request.user)

    context = {
        'form': form,
        'password_form': password_form,
    }

    return render(request, 'edit_profile.html', context)


def search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Destination.objects.filter(name__icontains=query)

            # Log search history
            if request.user.is_authenticated:
                SearchHistory.objects.create(user=request.user, query=query)
            else:
                SearchHistory.objects.create(query=query)

            # Update popularity count
            for result in results:
                result.popularity_count += 1
                result.save()

    return render(request, 'search.html', {'form': form, 'query': query, 'results': results})

def popular_places(request):
    # Define the time frame, e.g., last 7 days
    time_threshold = timezone.now() - timedelta(days=7)
    popular_places = Destination.objects.filter(searchhistory__timestamp__gte=time_threshold) \
                                        .annotate(search_count=models.Count('searchhistory')) \
                                        .order_by('-search_count')

    return render(request, 'welcome.html', {'popular_places': popular_places})

def write_review(request):
    form = SearchForm()
    places = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            places = Destination.objects.filter(name__icontains=query)

    return render(request, 'write_review.html', {'form': form, 'places': places})