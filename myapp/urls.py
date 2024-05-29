from django.urls import path
from .views import home, add_place, place_detail, register, profile, logout_view, edit_profile, search, write_review, add_review
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('add-place/', add_place, name='add-place'),
    path('place/<int:place_id>/', place_detail, name='place_detail'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('search/', search, name='search'),
    path('write-review/', write_review, name='write_review'),
    path('add-review/<int:pk>/', add_review, name='add_review'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)