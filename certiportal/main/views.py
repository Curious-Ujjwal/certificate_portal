from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import *
from .render import Render
from .forms import *
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from .choices import *
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator

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

    if candid.certificate_type == 'P': 
        return Render.render('certificate/certificateParticipation.html', context)
    elif candid.certificate_type == 'CA': 
        return Render.render('certificate/certificateCA.html', context)
    elif candid.certificate_type == 'W': 
        return Render.render('certificate/certificateWinner.html', context)


def isDuplicate(alcher_id, event, certificate_type, year):
    try:
        candid = candidate.objects.get(alcher_id=alcher_id, event=event, 
            certificate_type=certificate_type, year=year)
    except candidate.DoesNotExist:
        return False
    else:
        return True
    

def generateUrl(alcher_id , year):
    last_num = 0
    candid_certificates = candidate.objects.filter(alcher_id=alcher_id)
    if len(candid_certificates) > 0:  
        latest_cert = candid_certificates.last()
        arr = latest_cert.certificate_url.split('-')
        last_num = int(arr[4])
    new_url = alcher_id + '-' + str(year) + '-' + str(last_num+1)
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
            year = form.cleaned_data['year']
            email = form.cleaned_data['email']
            if not isDuplicate(alcher_id, event, certificate_type, year):
                new_url = generateUrl(alcher_id , year)
                candidate.objects.create(alcher_id=alcher_id, name=name, event=event, 
                    certificate_type=certificate_type, is_valid=True, is_generated=True, 
                    certificate_url=new_url, email=email, year=year)
            return redirect('candidList')
    else:
        form = CandidForm()
    
    return render(request, 'main/candidform.html', {'form':form} ) 

@login_required
def candidList(request):
    candids = candidate.objects.filter(year=current_year())
    context = {
        'candids': candids,
    }
    return render(request, 'main/candidlist.html', context)

@login_required
def send_email(request , alcher_id):
    try:
        candid = candidate.objects.get(alcher_id = alcher_id)
    except candidate.DoesNotExist:
        candid = None

    if not candid or not candid.is_valid:
    	#Candidate does not exist return to index.html
    	return render(request, 'registration/index.html')

    context = {
        'candid' : candid
    }

    send_mail(
        'Certificate Alcheringa: ' + str(current_year()),
         render_to_string('main/emails/mail.txt', context),
        'helpdesk@alcheringa.in',
        ['sidjain.24.sj@gmail.com'],
        fail_silently = False,
    )    

    return render(request, 'main/mail_sent.html')
    



def readDataFromCSV(csv_file):
    event_choices_list = [x[0] for x in EVENT_OPTIONS]
    certificate_choices_list = [x[0] for x in CERTIFICATE_OPTIONS]
    file_data = csv_file.read().decode("utf-8") 
    lines = file_data.split("\n")
    
    skipped_candids = []
    for line in lines:
        fields = line.split(",")
        if len(fields) < 5:
            continue

        alcher_id = fields[0].strip()        
        name = fields[1].strip()
        certificate_type = fields[2].strip()  
        event = fields[3].strip()
        year = fields[4].strip()
        email = fields[5].strip()

        try:
            email_validator = EmailValidator()
            alcher_id_validator = RegexValidator(r"ALC-[A-Z]{3}-[0-9]+")
            alcher_id_validator(alcher_id)
            email_validator(email)
        except ValidationError:
            skipped_candids.append((alcher_id,event))
            continue

        if certificate_type not in certificate_choices_list or event not in event_choices_list:
            skipped_candids.append((alcher_id,event))
            continue

        if not isDuplicate(alcher_id, event, certificate_type, year):
            new_url = generateUrl(alcher_id, year)
            candidate.objects.create(alcher_id=alcher_id, name=name, event=event, 
                certificate_type=certificate_type, is_valid=True, is_generated=True, 
                certificate_url=new_url, email=email, year=year)   
    return skipped_candids


@login_required
def candidBulk(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        context = {
        'form': CSVUploadForm(),
        }
        if form.is_valid():
            csv_file = request.FILES['file_CSV']
            if not csv_file.name.endswith('.csv'):
                messages.error(request,'ERROR!! File is not CSV type')
                return redirect('candidBulk')
            if csv_file.multiple_chunks():
                messages.error(request,"ERROR!! Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000))) 
                return redirect('candidBulk')
            skipped_candids = readDataFromCSV(csv_file)
            if len(skipped_candids)>0:
                context['skipped_candids'] = skipped_candids,
            messages.success(request, 'SUCCESS!! Data uploaded')

            return render(request, 'main/candidbulk.html', context)
    else:
        form = CSVUploadForm()
        return render(request, 'main/candidbulk.html', {'form':form}) 
