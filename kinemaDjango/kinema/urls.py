"""kinemaDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from . import views

urlpatterns = [
    path('', views.index, name="LandingPage"),
    path('movie/<int:id>/', views.MovieDetails, name="MovieDetails"),
    path('movies/', views.Movies, name="Movie"),
    path('cinema/<int:id>', views.CinemaDetails, name="CinemaDetails"),
    path('cinemas/', views.Cinemas, name="Cinemas"),
    path('top-movies/', views.TopMovies, name="TopMovies"),
    path('contacts/', views.Contacts, name="Contacts"),
    path('auth/', views.Auth, name="Auth"),
    path('reg/', views.Reg, name="Reg"),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('kinema:LandingPage')), name='logout'),
    path('movie/add_comment/<int:id>', views.movieSetComment, name='movieSetComment'),
    path('cinema/add_comment/<int:id>', views.cinemaSetComment, name='cinemaSetComment'),
    path('set_rate/<int:id>', views.setRating, name='setRating'),
    path('buy_ticket/<int:id>', views.BuyTicket, name='BuyTicket'),
    path('buy_ticket/<int:id>/step2', views.BuyTicket2, name='BuyTicket2'),
    path('buy_ticket/<int:id>/step3', views.BuyTicket3, name='BuyTicket3'),
    path('buy_ticket/<int:id>/final', views.BuyTicketFinal, name='BuyTicketFinal'),
    path('tickets/', views.Tickets, name='Tickets'),
    path('ticket/<int:id>', views.TicketInfo, name="TicketInfo")
]
