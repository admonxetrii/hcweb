import os, asyncio
from asgiref.sync import sync_to_async
from django.http import HttpResponse
from django.shortcuts import render, redirect
from LandingPage.models import ServicesDetail, HomeSlider, Projects, ProjectsPictures, TeamMembers, StaffCategory, \
    HomePageExtra, Certificates, Equipments
from adminpanel.models import QuotationRequest, ContactDetails
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from hcweb.settings import BASE_DIR
from email.mime.image import MIMEImage


# Create your views here.


def home(request):
    teams = TeamMembers.objects.all()[:3]
    servicedetail = ServicesDetail.objects.all()
    homeslider = HomeSlider.objects.all()
    projects = Projects.objects.all().order_by('-id')[:5]
    content = HomePageExtra.objects.get(id=1)
    context = {
        'teams': teams,
        'servicedetail': servicedetail,
        'homeslider': homeslider,
        'content': content,
        'projects': projects
    }
    return render(request, 'landing_index.html', context)


def about(request):
    homeslider = HomeSlider.objects.all()[:1]
    teams = TeamMembers.objects.all()[:3]
    context = {
        'flex': homeslider,
        'teams':teams
    }
    return render(request, 'about.html', context)


def projects(request):
    homeslider = HomeSlider.objects.all()[:1]
    completedp = Projects.objects.filter(is_completed=True)
    underp = Projects.objects.filter(is_completed=False)
    context = {
        'comp': completedp,
        'underp': underp,
        'flex': homeslider
    }
    return render(request, 'projects.html', context)


def manpower(request):
    homeslider = HomeSlider.objects.all()[:1]
    teamcategory = StaffCategory.objects.all()
    teams = TeamMembers.objects.all()
    context = {
        'flex': homeslider,
        'category': teamcategory,
        'teams': teams
    }
    return render(request, "teams.html", context)


def singleprojects(request, id):
    homeslider = HomeSlider.objects.all()[:1]
    project = Projects.objects.get(pk=id)
    recentp = Projects.objects.all().order_by('-id')[:3]
    images = ProjectsPictures.objects.filter(project_id=id)
    context = {
        'project': project,
        'images': images,
        'recentp': recentp,
        'flex': homeslider
    }
    return render(request, 'project_single.html', context)


def check_email_c(request):
    email = ContactDetails.objects.filter(email=request.POST.get('toemail'))
    if email.count():
        return HttpResponse('false')
    else:
        return HttpResponse('true')


def check_email_q(request):
    email = QuotationRequest.objects.filter(email=request.POST.get('toemail'))
    if email.count():
        return HttpResponse('false')
    else:
        return HttpResponse('true')


def contacts(request):
    homeslider = HomeSlider.objects.all()[:1]
    context = {
        'flex': homeslider
    }

    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        phone = request.POST.get('phone')
        toemail = request.POST.get('toemail')
        subject = request.POST.get('subject')
        message = request.POST.get('datamsg')

        emailcontext = {'fname': fname, 'lname': lname, 'email': toemail, 'phone': phone, 'type': 0}

        emailtouser(emailcontext)
        emailtooffice(emailcontext)

        ContactDetails.objects.create(fname=fname, lname=lname, phone=phone, email=toemail, subject=subject,
                                      message=message, is_responded=0)

        return HttpResponse('200')

    return render(request, 'contact.html', context)


def quotations(request):
    homeslider = HomeSlider.objects.all()[:1]
    context = {
        'flex': homeslider
    }
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        phone = request.POST.get('phone')
        toemail = request.POST.get('toemail')
        company = request.POST.get('company')
        project = request.POST.get('project')

        emailcontext = {'fname': fname, 'lname': lname, 'email': toemail, 'phone': phone, 'type': 1}

        emailtouser(emailcontext)
        emailtooffice(emailcontext)

        QuotationRequest.objects.create(fname=fname, lname=lname, phone=phone, email=toemail, about_company=company,
                                        about_project=project, is_responded=0)
        return HttpResponse('200')
    return render(request, 'quotation.html', context)


def newsletter(request):
    context = {
        'fname': 'Anonymous',
        'lname': 'User',
        'email': request.POST['email'],
        'phone': 'Null',
        'type': 2
    }
    emailtouser(context)
    return redirect('home')


def emailtouser(context):
    # send mail template
    if context["type"] == 0:
        emailsubject = "Thank you for contacting us."
        emailmessage = "Thank you for choosing Hanuman Construction. One of our staff will contact you very soon. Meanwhile visit our Projects page to find out completed projects and under progress projects."
    elif context["type"] == 1:
        emailsubject = "Quotation request received."
        emailmessage = "Thank you for choosing Hanuman Construction. One of our staff will provide you the quotation requested very soon. Meanwhile visit our Projects page to find out completed projects and under progress projects. "
    elif context["type"]==2:
        emailsubject = "Thank you for subscribing the newsletter of Hanuman Construction"
        emailmessage = "Thank you for subscribing Hanuman Construction. You will soon receive updates from the page directly to your email account. Meanwhile visit our Projects page to find out completed projects and under progress projects."

    html_content = render_to_string("email_template.html",
                                    {'fname': context["fname"], 'lname': context["lname"], 'toemail': context["email"],
                                     'phone': context["phone"],
                                     'emailmessage': emailmessage, 'subject': emailsubject, 'type': 1})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        emailsubject,
        text_content,
        settings.EMAIL_HOST_USER,
        [context["email"]]
    )
    email.attach_alternative(html_content, "text/html")

    for f in ["static/landingpage/images/hc-group.png", "static/landingpage/images/illo.png",
              "static/landingpage/images/bg_password.jpg"]:
        fp = open(os.path.join(BASE_DIR, f), 'rb')
        msg_img = MIMEImage(fp.read())
        fp.close()
        msg_img.add_header('Content-ID', '<{}>'.format(f))
        email.attach(msg_img)

    email.send()


def emailtooffice(context):
    # send mail template
    if context["type"] == 0:
        emailsubject = "Someone tried to contact through your website"
        emailmessage = "Dear admin, Kindly check the contact page from the admin panel of the website of Hanuman Construction. One of the page visitor recently tried to contact the company via website. Please respond them as soon as possible. You can respond to them via your admin panel. You can find all the details through the admin panel."
    elif context["type"] == 1:
        emailsubject = "Somebody has requested quotation for thier project"
        emailmessage = "Dear admin, Kindly check the quotation page from the admin panel of the website of Hanuman Construction. One of the page visitor has requested the quotation for their project via the company via website. Please respond them as soon as possible. You can respond to them via your admin panel. You can find all the details through the admin panel."
    html_content = render_to_string("email_template.html",
                                    {'fname': 'Admin', 'lname': 'department', 'emailmessage': emailmessage,
                                     'subject': emailsubject})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        emailsubject,
        text_content,
        settings.EMAIL_HOST_USER,
        ['admonwg@gmail.com']
    )
    email.attach_alternative(html_content, "text/html")

    for f in ["static/landingpage/images/hc-group.png", "static/landingpage/images/illo.png",
              "static/landingpage/images/bg_password.jpg"]:
        fp = open(os.path.join(BASE_DIR, f), 'rb')
        msg_img = MIMEImage(fp.read())
        fp.close()
        msg_img.add_header('Content-ID', '<{}>'.format(f))
        email.attach(msg_img)

    email.send()


def certificate(request):
    flex = HomeSlider.objects.all()[:1]
    cert = Certificates.objects.all()
    context = {
        'flex':flex,
        'cert':cert
    }
    return render(request, "certificate.html", context)

def equipments(request):
    flex = HomeSlider.objects.all()[:1]
    equip = Equipments.objects.all()
    context = {
        'flex':flex,
        'equip':equip
    }
    return render(request, "equipments.html", context)

def cprofile(request):
    flex = HomeSlider.objects.all()[:1]
    context = {
        'flex': flex,
    }
    return render(request, "cprofile.html", context)