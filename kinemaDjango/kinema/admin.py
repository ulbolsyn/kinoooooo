from django.contrib import admin
from .models import *

# Movie
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name']

class YearAdmin(admin.ModelAdmin):
    list_display = ['value']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class DirectorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']

class ActorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']

class MovieImageInline(admin.TabularInline):
    model = MovieImage
    raw_id_field = ['movie_img']

class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'duration', 'year', 'director', 'link_trailer', 'link_poster']
    inlines = [MovieImageInline]

class RateAdmin(admin.ModelAdmin):
    list_display = ['rate', 'user', 'movie']

class CommentMovieAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie']

# Cinema
class CinemaImageInline(admin.TabularInline):
    model = CinemaImage
    raw_id_field = ['cinema_img']

class CinemaAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'phone']
    inlines = [CinemaImageInline]

class ShowTimeInline(admin.TabularInline):
    model = ShowTime
    raw_id_field = ['time']

class CinemaMovieAdmin(admin.ModelAdmin):
    list_display = ['cinema', 'movie']
    inlines = [ShowTimeInline]

class CommentCinemaAdmin(admin.ModelAdmin):
    list_display = ['user', 'cinema']

class TicketAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'cinema', 'date', 'cost', 'sits']

admin.site.register(Country, CountryAdmin)
admin.site.register(Year, YearAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Director, DirectorAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Rate, RateAdmin)
admin.site.register(CommentMovie, CommentMovieAdmin)
admin.site.register(Cinema, CinemaAdmin)
admin.site.register(CinemaMovie, CinemaMovieAdmin)
admin.site.register(CommentCinema, CommentCinemaAdmin)
admin.site.register(Ticket, TicketAdmin)
