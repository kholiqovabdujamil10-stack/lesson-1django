from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import *


def registration(request):
    if request.method == 'POST':
        data = request.POST
        if data:
            User.objects.create_user(username=data['username'], password=data['password'])
        else:
            return redirect("registration")
        return redirect("login")
    return render(request, 'registration.html')


def login_user(request):
    if request.method == 'POST':
        data = request.POST
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            return redirect('login')
    return render(request, 'login.html')


@login_required
def home(request):
    sports = Sport.objects.all()
    games = Game.objects.all()
    today = datetime.now().date()
    today_games = [game for game in games if game.date.date() == today]
    upcoming_games = [game for game in games if game.date.date() > today and game.status == 'scheduled']
    return render(request, 'home.html', {'sports': sports, 'today_games': today_games, 'upcoming_games': upcoming_games})


@login_required
def logout_user(request):
    logout(request)
    return redirect("login")


@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
def create_game(request):
    if request.method == 'POST':
        data = request.POST
        Game.objects.create(
            sport=get_object_or_404(Sport, id=data['sport']),
            home_team=get_object_or_404(Team, id=data['home_team']),
            away_team=get_object_or_404(Team, id=data['away_team']),
            date=data['date'],
            stadium=data['stadium'],
            ticket_price=data['ticket_price'],
            available_tickets=data['available_tickets'],
            created_by=request.user
        )
        return redirect('home')
    return render(request, 'create_game.html', {'sports': Sport.objects.all(), 'teams': Team.objects.all()})


@login_required
def edit_game(request, id):
    game = get_object_or_404(Game, id=id, created_by=request.user)
    if request.method == 'POST':
        data = request.POST
        game.sport = get_object_or_404(Sport, id=data['sport'])
        game.home_team = get_object_or_404(Team, id=data['home_team'])
        game.away_team = get_object_or_404(Team, id=data['away_team'])
        game.date = data['date']
        game.stadium = data['stadium']
        game.ticket_price = data['ticket_price']
        game.available_tickets = data['available_tickets']
        game.save()
        return redirect('home')
    return render(request, 'edit_game.html', {'game': game, 'sports': Sport.objects.all(), 'teams': Team.objects.all()})


@login_required
def delete_game(request, id):
    game = get_object_or_404(Game, id=id, created_by=request.user)
    if request.method == 'POST':
        if Ticket.objects.filter(game=game).exists():
            return render(request, 'delete_game.html', {'game': game, 'error': 'Cannot delete this game because tickets have already been purchased.'})
        game.delete()
        return redirect('home')
    
    return render(request, 'delete_game.html', {'game': game})


@login_required
def games(request):
    games = Game.objects.all().order_by('date')
    return render(request, 'games.html', {'games': games})


@login_required
def buy_ticket(request, id):
    game = get_object_or_404(Game, id=id)

    if request.method == 'POST':
        data = request.POST
        quantity = int(data['quantity'])
        if quantity > 0 and quantity <= game.available_tickets:
            Ticket.objects.create(user=request.user, game=game, quantity=quantity, price=game.ticket_price * quantity, status='paid')
            game.available_tickets -= quantity
            game.save()
            return redirect('my_tickets')
        return redirect('home')
    return render(request, 'buy_ticket.html', {'game': game})


@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'my_tickets.html', {'tickets': tickets})


@login_required
def cancel_ticket(request, id):
    ticket = get_object_or_404(Ticket, id=id, user=request.user)

    if request.method == 'POST':
        ticket.game.available_tickets += ticket.quantity
        ticket.game.save()
        ticket.status = 'cancelled'
        ticket.save()
        return redirect('my_tickets')
    return render(request, 'cancel_ticket.html', {'ticket': ticket})