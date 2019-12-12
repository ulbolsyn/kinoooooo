from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.urls import resolve
from django.core.paginator import Paginator
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .forms import *
from django.contrib.auth import login, authenticate
from django.utils import timezone

def index(request):
    movies = Movie.objects.order_by('-id')
    return render(request, 'kinema/index.html', {'today_choice': movies[0:6],
                                                 'now_in_cinema': movies[0:8]})

def MovieDetails(request, id):
    try:
        rate = rate = Rate.objects.get(movie__id=id, user=request.user)
    except:
        rate = None
    return render(request, 'kinema/movie_details.html', {'movie': get_object_or_404(Movie, id=id),
                                                         'cinemas': CinemaMovie.objects.filter(movie=get_object_or_404(Movie, id=id)),
                                                         'rating': rate})

def Movies(request):
    movies = Movie.objects.order_by('-releas_date')
    years = Year.objects.order_by('-value')
    cinemas = Cinema.objects.order_by('name')
    categories = Category.objects.order_by('name')
    paginator = Paginator(movies, 4)
    page = request.GET.get('page')
    movie_list = paginator.get_page(page)
    next_page = movie_list.next_page_number() if movie_list.has_next() else page
    prev_page = movie_list.previous_page_number() if movie_list.has_previous() else page
    return render(request, 'kinema/movies.html', {'movies': movie_list.object_list,
                                                  'has_other': movie_list.has_other_pages(),
                                                  'has_next': movie_list.has_next(),
                                                  'has_prev': movie_list.has_previous(),
                                                  'next_page': next_page,
                                                  'prev_page': prev_page,
                                                  'years': years,
                                                  'cinemas': cinemas,
                                                  'categories': categories})

def CinemaDetails(request, id):
    return render(request, 'kinema/cinema_details.html', {'cinema': get_object_or_404(Cinema, id=id)})

def Cinemas(request):
    cinemas = Cinema.objects.order_by('name')
    paginator = Paginator(cinemas, 8)
    page = request.GET.get('page')
    cinima_list = paginator.get_page(page)
    next_page = cinima_list.next_page_number() if cinima_list.has_next() else page
    prev_page = cinima_list.previous_page_number() if cinima_list.has_previous() else page
    return render(request, 'kinema/cinemas.html', {'cinemas': cinima_list.object_list,
                                                  'has_other': cinima_list.has_other_pages(),
                                                  'has_next': cinima_list.has_next(),
                                                  'has_prev': cinima_list.has_previous(),
                                                  'next_page': next_page,
                                                  'prev_page': prev_page})

def TopMovies(request):
    return render(request, 'kinema/top-movies.html', {'movies': sorted(Movie.objects.all(), key=lambda t: t.rate)[0:20]})

def Contacts(request):
    return render(request, 'kinema/contacts.html')

def Auth(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login_user = authenticate(username=username, password=password)

        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('kinema:LandingPage'))

    return render(request, 'kinema/auth.html', {'form': form})

def Reg(request):
    try:
        form = RegistrationForm(request.POST or None)

        if form.is_valid():
            new_user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            new_user.username = username
            new_user.set_password(password)
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.email = email
            new_user.save()
            login_user = authenticate(username=username, password=password)

            if login_user:
                login(request, login_user)
                return HttpResponseRedirect(reverse_lazy('kinema:LandingPage'))
        return render(request, 'kinema/reg.html', {'form': form})
    except:
        raise Http404('Something maybe you entered the data incorrectly')

def movieSetComment(request, id):
    try:
        if request.POST.get("comment_text") == '':
            return HttpResponse('Empty')
        comment_text = request.POST.get("comment_text")
        comment = CommentMovie(comment = comment_text, user = request.user, movie=get_object_or_404(Movie, id=id), posted=timezone.now())
        comment.save()
        return redirect(request.META.get('HTTP_REFERER'))
    except:
        return redirect(request.META.get('HTTP_REFERER'))

def cinemaSetComment(request, id):
    try:
        if request.POST.get("comment_text") == '':
            return HttpResponse('Empty')

        comment_text = request.POST.get("comment_text")
        comment = CommentCinema(comment = comment_text, user = request.user, cinema=get_object_or_404(Cinema, id=id), posted=timezone.now())
        comment.save()
        return redirect(request.META.get('HTTP_REFERER'))
    except:
        return redirect(request.META.get('HTTP_REFERER'))

def setRating(request, id):
    try:
        movie = get_object_or_404(Movie, id=id)
        user = User.objects.get(id=request.user.id)
        rating_num = int(request.POST['rating_num'])
        new_rating = Rate(user=user, movie=movie, rate=rating_num)
        new_rating.save()

        return redirect(request.META.get('HTTP_REFERER'))

    except:
        return redirect(request.META.get('HTTP_REFERER'))

def BuyTicket(request, id):
    return render(request, 'kinema/book1.html', {'movie': get_object_or_404(Movie, id=id),
                                                 'cinemas': CinemaMovie.objects.filter(movie=get_object_or_404(Movie, id=id))})

def BuyTicket2(request, id):
    cinema = request.POST.get("choosen-cinema")
    date = request.POST.get("choosen-date")
    time = request.POST.get("choosen-time")
    if (cinema == ""):
        return BuyTicket(request, id)
    return render(request, 'kinema/book2.html', {'movie': get_object_or_404(Movie, id=id),
                                                 'cinemas': CinemaMovie.objects.filter(movie=get_object_or_404(Movie, id=id)),
                                                 'cinema': cinema,
                                                 'date': date,
                                                 'time': time})

def BuyTicket3(request, id):
    cinema = request.POST.get("choosen-cinema")
    date = request.POST.get("choosen-date")
    time = request.POST.get("choosen-time")
    count_ticket = request.POST.get("choosen-number")
    count_10 = request.POST.get("choosen-number--cheap")
    count_20 = request.POST.get("choosen-number--middle")
    count_30 = request.POST.get("choosen-number--expansive")
    cost = request.POST.get("choosen-cost")
    sits = request.POST.get("choosen-sits")
    if (count_ticket == ""):
        return BuyTicket2(request, id)
    return render(request, 'kinema/book3-buy.html', {'movie': get_object_or_404(Movie, id=id),
                                                     'cinemas': CinemaMovie.objects.filter(movie=get_object_or_404(Movie, id=id)),
                                                     'cinema': cinema,
                                                     'date': date,
                                                     'time': time,
                                                     'count_ticket': count_ticket,
                                                     'count_10': count_10,
                                                     'count_20': count_20,
                                                     'count_30': count_30,
                                                     'cost': cost,
                                                     'sits': sits})

def BuyTicketFinal(request, id):
    cinema = request.POST.get("choosen-cinema")
    date = request.POST.get("choosen-date")
    time = request.POST.get("choosen-time")
    count_ticket = request.POST.get("choosen-number")
    count_10 = request.POST.get("choosen-number--cheap")
    count_20 = request.POST.get("choosen-number--middle")
    count_30 = request.POST.get("choosen-number--expansive")
    cost = request.POST.get("choosen-cost")
    sits = request.POST.get("choosen-sits")
    mail = request.POST.get("user-mail")
    tel = request.POST.get("user-tel")
    ticket = Ticket(user=request.user, cinema=Cinema.objects.get(name__contains=cinema), movie=get_object_or_404(Movie, id=id),date=date, time=time, count=int(count_ticket), count_10=int(count_10), count_20=int(count_20), count_30=int(count_30), cost=int(cost), sits=sits, mail=mail, phone=tel)
    ticket.save()
    return render(request, 'kinema/book-final.html', {'movie': get_object_or_404(Movie, id=id),
                                                     'cinemas': CinemaMovie.objects.filter(movie=get_object_or_404(Movie, id=id)),
                                                     'cinema': cinema,
                                                     'date': date,
                                                     'time': time,
                                                     'count_ticket': count_ticket,
                                                     'count_10': count_10,
                                                     'count_20': count_20,
                                                     'count_30': count_30,
                                                     'cost': cost,
                                                     'sits': sits,
                                                     'mail': mail,
                                                     'tel': tel})

def Tickets(request):
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'kinema/tickets.html', {'tickets': tickets})

def TicketInfo(request, id):
    ticket = Ticket.objects.get(id=id)
    return render(request, 'kinema/book-final.html', {'movie': Movie.objects.get(id=ticket.movie.id),
                                                     'cinemas': CinemaMovie.objects.filter(movie=get_object_or_404(Movie, id=ticket.movie.id)),
                                                     'cinema': ticket.cinema.name,
                                                     'date': ticket.date,
                                                     'time': ticket.time,
                                                     'count_ticket': ticket.count,
                                                     'count_10': ticket.count_10,
                                                     'count_20': ticket.count_20,
                                                     'count_30': ticket.count_30,
                                                     'cost': ticket.cost,
                                                     'sits': ticket.sits,
                                                     'mail': ticket.mail,
                                                     'tel': ticket.phone})
