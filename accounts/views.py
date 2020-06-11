from django.shortcuts import render


def profile(request):
    pass

def login(request):
    pass

def signup(request):
    return render(request, 'accounts/form.html')

def logout(request):
    pass

def update(request):
    pass

def delete(request):
    pass