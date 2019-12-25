from django.shortcuts import render
from django.contrib.auth import logout

# Create your views here.
def index(request):
    return render(request , 'registration/index.html')

def logout(request):
    return render(request , 'registration/logout.html')

# def logout_view(request):
#     logout(request)
#     return render(request , 'registration/logout.html')
#     # Redirect to a success page.