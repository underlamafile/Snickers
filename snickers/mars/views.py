from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from .models import Post
from django.utils import timezone


# Create your views here.
def index(request):
    return render(request, 'mars/index.html', {
        'name': 'user',
        'age': '228',
        'list': ['1', '2', '3'],
        'dict': [
            {'main': {
                'name': 'igorek',
                'age': '322'
            }},
            {'main': {
                'name': 'aren',
                'age': '1488'
            }},
        ]
    })


def turtle(request):
    return render(request, 'mars/turtle.html', {})


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'mars/post_list.html', {'posts': posts})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('login')
        else:
            return render(request, 'registration/register.html', {'form': form})

    form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
