import json
# from django.urls import reverse_lazy
from django.views import generic

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from .models import Players, CustomUser, Wiki, News


def sign_up(request):
    form_class = CustomUserCreationForm
    # success_url = reverse_lazy('login')
    # template_name = 'signup.html'
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = form_class() # this is important

    return render(request, 'signup.html', {
        'form': form,  # NOTE: instead of form_class!!!!
        })

@login_required
def get_context_data(self, **kwargs):
    context['my_dictionary'] = json.dumps(self.object.mydict)

def login_page(request):
    return render(request, 'accounts/login.html')

@login_required
def play(request):
    wiki = Wiki.objects.all()
    return render(request, 'client.html', {'user': CustomUser, 'wiki': wiki})

def index(request):
    news = News.objects.all()
    return render(request, 'home.html', {'news': news})

# @login_required
# def wiki_list(request, pk):
#     wiki = Wiki.objects.all()
#     # (order_by('title'))
#     return render(request, 'wiki_base.html', {'wiki': wiki})