from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import models
from .serializers import MainCycleSerializer, BoostSerializer

# Create your views here.
def index(request):
    try:
        user = models.User.objects.get(id=request.user.id)
    except:
        form = UserCreationForm(request.POST)
        return render(request, 'registration/register.html', {'form': form})
        quit()

    maincycle = models.MainCycle.objects.get(user=request.user)
    boosts = models.Boost.objects.filter(main_cycle=maincycle)

    return render(request, 'mars/index.html', {
        'maincycle': maincycle,
        'boosts': boosts,
    })


def turtle(request):
    return render(request, 'mars/turtle.html', {})

def work(request):
    return render(request, 'mars/work.html', {})


@api_view(['GET'])
def call_click(request):
    maincycle = models.MainCycle.objects.get(user=request.user)
    is_boost_created = maincycle.click()
    maincycle.save()

    if is_boost_created:
        boost_type = 0
        if maincycle.level % 3 == 0:
            boost_type = 1

        boost = models.Boost(main_cycle=maincycle, power=maincycle.level * 20, price=maincycle.level * 50,
                             boost_type=boost_type)
        boost.save()

        return Response({
            'main_cycle': MainCycleSerializer(maincycle).data,
            'boost': BoostSerializer(boost).data,
        })
    return Response({
        'main_cycle': MainCycleSerializer(maincycle).data,
    })


@api_view(['POST'])
def update_boost(request):
    boost_id = request.data['boost_id']
    maincycle = models.MainCycle.objects.get(user=request.user)

    boost = models.Boost.objects.get(id=boost_id)
    boost.update_boost()
    boost.save()

    return Response({
        'main_cycle': MainCycleSerializer(maincycle).data,
        'boost': BoostSerializer(boost).data,
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            main_cycle = models.MainCycle()
            main_cycle.user = user
            main_cycle.save()

            boost = models.Boost(main_cycle=main_cycle)
            boost.save()

            return redirect('login')
        else:
            return render(request, 'registration/register.html', {'form': form})

    form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


