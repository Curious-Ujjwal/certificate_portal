from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import *
from .render import Render
from .forms import *

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


def isDuplicate(alcher_id, event, certificate_type):
    try:
        candid = candidate.objects.get(alcher_id=alcher_id, event=event, 
            certificate_type=certificate_type, year=2020 )       ########### Have to change it every year !!!
    except candidate.DoesNotExist:
        return False
    else:
        return True
    

def generateUrl(alcher_id):
    last_num = 0
    candid_certificates = candidate.objects.filter(alcher_id=alcher_id)
    if len(candid_certificates) > 0:  
        latest_cert = candid_certificates.last()
        arr = latest_cert.certificate_url.split('-')
        last_num = int(arr[4])
        print(latest_cert.certificate_type)
    new_url = alcher_id+'-2020-'+str(last_num+1)  ########### Have to change it every year !!!
    return new_url


@login_required
def candidForm(request):
    if request.method == 'POST':
        form = CandidForm(request.POST)
        if form.is_valid():
            alcher_id = form.cleaned_data['alcher_id']
            name = form.cleaned_data['name']
            event = form.cleaned_data['event']
            certificate_type = form.cleaned_data['certificate_type']
            if not isDuplicate(alcher_id, event, certificate_type):
                new_url = generateUrl(alcher_id)
                candidate.objects.create(alcher_id=alcher_id, name=name, event=event, 
                    certificate_type=certificate_type, is_valid=True, is_generated=True, 
                    certificate_url=new_url, year=2020)           ########### Have to change it every year !!!
            return redirect('candidList')
    else:
        form = CandidForm()
    
    return render(request, 'main/candidform.html', {'form':form}) 

@login_required
def candidList(request):
    candids = candidate.objects.filter(year=2020)               ########### Have to change it every year !!!
    context = {
    'candids': candids,
    }
    return render(request, 'main/candidlist.html', context)