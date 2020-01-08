from django.shortcuts import render
from django.contrib.auth import logout
from .models import *
from .render import Render


# Create your views here.
def index(request):
    return render(request , 'registration/index.html')

def logoutView(request):
    logout(request)
    return render(request , 'registration/logout.html')



def certificate(request, cert_id):
    
    try:
        candid = candidate.objects.get(certificate_url=cert_id)
    except candidate.DoesNotExist:
        candid = None

    if not candid or not candid.is_valid:
    	# DO SOMETHING 
    	return render(request, 'registration/index.html')

    context = {
        candid = candid,
    }
    return Render.render('certificate/certificateParticipant.html', context)

