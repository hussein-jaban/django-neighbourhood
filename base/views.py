from django.shortcuts import render, redirect
from django.contrib import messages
from base.models import User, Post, NeighbourHood, Business
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from cloudinary.forms import cl_init_js_callbacks



# Create your views here.

def home(request):
   return render(request, 'landing.html')
  
def loginPage(request):
   if request.user.is_authenticated:
     return redirect('home')
   if request.method == 'POST':
     email = request.POST['email'].lower()
     password = request.POST['password']
     print(email)
     print(password)
     try:
         user = User.objects.get(email=email)
     except:
         messages.error(request, 'User not exist.')
         
     user = authenticate(request, email=email, password=password)
     if user:
         login(request, user)
         
         return redirect('neighbour')
     else:
         messages.error(request, 'Email or password incorrect.')
   return render(request, 'login.html')
  

def registerPage(request):
   if request.user.is_authenticated:
       return redirect('home')
   
   context = {'form':'form'}
   if request.method == 'POST':
        if User.objects.filter(username=request.POST['username']).exists():
          messages.info(request, 'Username is taken')
          return render(request, 'register.html')
        elif User.objects.filter(email=request.POST['email']).exists():
          messages.info(request, 'Email is taken')
          return render(request, 'register.html')
        elif request.POST['password1'] != request.POST['password2']:
          messages.info(request, 'Password and Confirm Password do not match')
          return render(request, 'register.html')
        elif request.POST['neighboor'] == 'no' :
          messages.info(request, 'Select a neighboorhood')
          return render(request, 'register.html')
        elif len(request.POST['password1']) < 8 or request.POST['password1'] == request.POST['username']:
          messages.info(request, 'Password length must be > 9 & not the same as username')
          return render(request, 'register.html')
        else:
           print('you have reached user creating')
           print(request.POST)
           user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password1'], neighboorhood=request.POST['neighboor'])
           user.save()
           login(request, user)
           return redirect('neighbour')
   return render(request, 'register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')
 
@login_required(login_url='loginPage')
def neighbour(request):
   neighbour = NeighbourHood.objects.get(name=request.user.neighboorhood)
   posts = Post.objects.filter(neighbourHood=neighbour)
   businesses = Business.objects.filter(neighbourHood=neighbour)
   context = {'posts':posts, 'businesses':businesses}
   return render(request, 'neighbourhood.html', context)