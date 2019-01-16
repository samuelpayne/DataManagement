from django.shortcuts import render

#Create general views here.

def home(request):
    return render(request, 'home.html')
