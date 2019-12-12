from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User

class Country(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name="Country", default="Contry Name")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        index_together = [
            ['id', 'name']
        ]
        verbose_name = "Country"
        verbose_name_plural = "Countries"

class Year(models.Model):
    value = models.PositiveIntegerField(db_index=True, verbose_name="Year", default=2000)

    def __str__(self):
        return str(self.value)

    class Meta:
        ordering = ['value']
        index_together = [
            ['id', 'value']
        ]
        verbose_name = "Year"
        verbose_name_plural = "Years"

class Category(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name="Category", default="Category Name")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        index_together = [
            ['id', 'name']
        ]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Director(models.Model):
    first_name = models.CharField(max_length=20, db_index=True, verbose_name="First Name",  default="FName")
    last_name = models.CharField(max_length=20, db_index=True, verbose_name="Last Name", default="LName")

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        ordering = ['first_name']
        index_together = [
            ['id', 'first_name', 'last_name']
        ]
        verbose_name = "Director"
        verbose_name_plural = "Directors"

class Actor(models.Model):
    first_name = models.CharField(max_length=20, db_index=True, verbose_name="First Name", default="FName")
    last_name = models.CharField(max_length=20, db_index=True, verbose_name="Last Name", default="LName")

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        ordering = ['first_name']
        index_together = [
            ['id', 'first_name', 'last_name']
        ]
        verbose_name = "Actor"
        verbose_name_plural = "Actors"

class Movie(models.Model):
    name = models.CharField(max_length=75, db_index=True, verbose_name="Name", default="Movie Name")
    duration = models.DurationField(default=timedelta(), verbose_name="Duration")
    countries = models.ManyToManyField(Country, verbose_name="Countries")
    year = models.ForeignKey(Year, on_delete=models.CASCADE, verbose_name="Year")
    categories = models.ManyToManyField(Category, verbose_name="Categories")
    releas_date = models.DateTimeField(verbose_name="Release Date")
    director = models.ForeignKey(Director, verbose_name="Director", on_delete=models.CASCADE)
    actors = models.ManyToManyField(Actor, verbose_name="Actors")
    age_restrict = models.PositiveIntegerField(verbose_name="Age Restriction",  default=0)
    box_office = models.PositiveIntegerField(verbose_name="Box Office", default=1000)
    plot = models.TextField(verbose_name="The Plot", default="This is the plot of Movie")
    link_trailer = models.URLField(verbose_name="Link to Trailer", default="https://www.youtube.com/watch?v=hHW1oY26kxQ")
    link_poster = models.URLField(verbose_name="Link to Poster", default="https://www.quantabiodesign.com/wp-content/uploads/No-Photo-Available.jpg")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        index_together = [
            ['id', 'name']
        ]
        verbose_name = "Movie"
        verbose_name_plural = "Movies"

    @property
    def rate(self):
        rates = Rate.objects.filter(movie=self)
        count = len(rates)
        rates = sum(i.rate for i in rates)
        if count == 0:
            return 0
        return rates / count
    @property
    def rate_len(self):
        return len(Rate.objects.filter(movie=self))
    @property
    def comments(self):
        return CommentMovie.objects.filter(movie=self)
    @property
    def images(self):
        return MovieImage.objects.filter(movie=self)
    @property
    def comment_count(self):
        return len(self.comments)
    @property
    def categories_list(self):
        return self.categories.all()
    @property
    def country_list(self):
        return self.countries.all()
    @property
    def actors_list(self):
        return self.actors.all()
    @property
    def image_count(self):
        return len(self.images)
    @property
    def cinemas(self):
        return CinemaMovie.objects.filter(movie=self)
    @property
    def cinemas_len(self):
        return len(self.cinemas)

class MovieImage(models.Model):
    movie = models.ForeignKey(Movie, verbose_name="Movie", related_name="movie_img", on_delete=models.CASCADE)
    movie_img = models.ImageField(upload_to='images/', blank=True, verbose_name="Image")

class Rate(models.Model):
    rate = models.FloatField(verbose_name="Rate")
    user = models.ForeignKey(User, verbose_name="Rated User", related_name="users", on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, verbose_name="Movie", related_name="movie", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " rated " + str(self.rate) + " to " + self.movie.name

    class Meta:
        ordering = ['user']
        verbose_name = "Rate"
        verbose_name_plural = "Rates"

class Cinema(models.Model):
    name = models.CharField(max_length=75, db_index=True, verbose_name="Name", default="Cinema Name")
    address = models.CharField(max_length=75, verbose_name="Adress", default="Address")
    phone = models.CharField(max_length=75, verbose_name="Phone", default="Phone")
    website = models.URLField(verbose_name="Link to Cinema Site", default="http://www.kinopark.kz/ru")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Cinema"
        verbose_name_plural = "Cinemas"
    @property
    def comments(self):
        return CommentCinema.objects.filter(cinema=self)
    @property
    def images(self):
        return CinemaImage.objects.filter(cinema=self)
    @property
    def comment_count(self):
        return len(self.comments)
    @property
    def preview_img(self):
        return self.images[0].cinema_img

class CinemaImage(models.Model):
    cinema = models.ForeignKey(Cinema, verbose_name="Cinema", related_name="cinema_img", on_delete=models.CASCADE)
    cinema_img = models.ImageField(upload_to='images/', blank=True, verbose_name="Image")

class CinemaMovie(models.Model):
    cinema = models.ForeignKey(Cinema, verbose_name="Cinema", related_name="cinema_m", on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, verbose_name="Movie", related_name="movie_c", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.cinema) + " " + str(self.movie)

    class Meta:
        ordering = ['cinema']
        verbose_name = "Show Time List"
        verbose_name_plural = "Show Time Lists"

    @property
    def times(self):
        return ShowTime.objects.filter(cinema_movie=self)

class ShowTime(models.Model):
    cinema_movie = models.ForeignKey(CinemaMovie, verbose_name="Cinema Movie", related_name="cinema_movie", on_delete=models.CASCADE)
    time = models.TimeField(auto_now=False, auto_now_add=False, verbose_name="Show Time")

class CommentMovie(models.Model):
    comment = models.TextField(verbose_name="Comment", default="This is the comment to Movie")
    user = models.ForeignKey(User, verbose_name="Commented User", related_name="user_m", on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, verbose_name="Movie", related_name="movie_cm", on_delete=models.CASCADE)
    posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " comment to " + self.movie.name

    class Meta:
        ordering = ['user']
        verbose_name = "Comment to Movie"
        verbose_name_plural = "Comments to Movies"

class CommentCinema(models.Model):
    comment = models.TextField(verbose_name="Comment", default="This is the comment to Cinema")
    user = models.ForeignKey(User, verbose_name="Commented User", related_name="user_c", on_delete=models.CASCADE)
    cinema = models.ForeignKey(Cinema, verbose_name="Cinema", related_name="cinema_cm", on_delete=models.CASCADE)
    posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " comment to " + self.cinema.name

    class Meta:
        ordering = ['user']
        verbose_name = "Comment to Cinema"
        verbose_name_plural = "Comments to Cinemas"

class Ticket(models.Model):
    user = models.ForeignKey(User, verbose_name="Buyer", related_name="user_t", on_delete=models.CASCADE)
    cinema = models.ForeignKey(Cinema, verbose_name="Cinema", related_name="cinema_t", on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, verbose_name="Movie", related_name="movie_t", on_delete=models.CASCADE)
    date = models.CharField(verbose_name="Date", max_length=20, default="0")
    time = models.CharField(verbose_name="Time", max_length=20, default="0")
    count = models.PositiveIntegerField(verbose_name="Count of Tickets")
    count_10 = models.PositiveIntegerField(verbose_name="Count of $10 Tickets")
    count_20 = models.PositiveIntegerField(verbose_name="Count of $20 Tickets")
    count_30 = models.PositiveIntegerField(verbose_name="Count of $30 Tickets")
    cost = models.PositiveIntegerField(verbose_name="Price of all Tickets")
    sits = models.CharField(max_length=200, verbose_name="Sits of Ticket")
    mail = models.CharField(max_length=200, verbose_name="Mail")
    phone = models.CharField(max_length=15, verbose_name="Phone")

    def __str__(self):
        return self.user.username + " Ticket to " + self.movie.name + " " + self.date

    class Meta:
        ordering = ['id']
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
