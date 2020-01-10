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
        'candid_name' : candid.name,
        'candid_alcher_id' : candid.alcher_id,

    }
    print(candid.alcher_id)
    if candid.certificate_type == 'P': 
        return Render.render('certificate/certificateParticipation.html', context)
    if candid.certificate_type == 'CA': 
        return Render.render('certificate/certificateCA.html', context)
    if candid.certificate_type == 'W': 
        return Render.render('certificate/certificateWinner.html', context)

