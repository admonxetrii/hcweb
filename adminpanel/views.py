import time, os

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from hcweb.settings import BASE_DIR
from email.mime.image import MIMEImage

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from .models import QuotationRequest, ContactDetails
from LandingPage.models import ServicesDetail, HomeSlider, Projects, ProjectsPictures, StaffCategory, StaffSubCategory, \
    TeamMembers, HomePageExtra
from .forms import ServiceDetailForm, HomeSliderForm, StaffCategoryForm, StaffSubCategoryForm, TeamMembersForms
from django.contrib import messages


# Create your views here.

def signin(request):
    if request.user.is_authenticated:
        return redirect('adminhome')
    if request.method == 'GET':
        return render(request, 'signin.html')
    else:
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('adminhome')
        else:
            messages.add_message(request, messages.ERROR, "Your username and password doesn't match!!!")
            return redirect('signin')


def signout(request):
    logout(request)
    messages.add_message(request, messages.ERROR, "You've been logged out!")
    return redirect('signin')

@login_required(login_url='signin')
def homepageextra(request):
    contents = HomePageExtra.objects.get(id=1)
    context = {
        'content': contents
    }
    if request.method == 'POST':
        projects = request.POST['projects']
        employees = request.POST['employees']
        ongoing = request.POST['ongoing']
        partners = request.POST['partners']
        contents.numberofprj = projects
        contents.numberofemp = employees
        contents.numberofconst = ongoing
        contents.numberofpart = partners
        try:
            coverimg = request.FILES['coverimg']
        except MultiValueDictKeyError:
            coverimg = contents.image
        if coverimg:
            contents.image = coverimg
        contents.save()
        messages.add_message(request, messages.SUCCESS, "Data edited successfully.")
    return render(request, "admin_extra.html", context)


@login_required(login_url='signin')
def homeslideradmin(request):
    data = HomeSlider.objects.all()
    form = HomeSliderForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Slider added successfully!")
            return redirect('adminhome')
    context = {
        'form': form,
        'data': data
    }
    return render(request, 'admin_index.html', context)


@login_required(login_url='signin')
def edithomeslider(request, id):
    data = HomeSlider.objects.get(id=id)
    form = HomeSliderForm(request.POST or None, request.FILES or None, instance=data)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Slider edited successfully!")
            return redirect('adminhome')
    context = {
        'form': form,
        'data': data
    }
    return render(request, 'admin_editHomeSlider.html', context)


@login_required(login_url='signin')
def delhomeslider(request, id):
    data = HomeSlider.objects.get(id=id)
    data.delete()
    messages.add_message(request, messages.ERROR, "Slider deleted successfully!")
    return redirect('adminhome')


@login_required(login_url='signin')
def servicedetailadmin(request):
    data = ServicesDetail.objects.all()
    form = ServiceDetailForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Tabs added successfully!")
            return redirect('servicedetailadmin')
    context = {
        'form': form,
        'data': data
    }
    return render(request, 'admin_servicedetail.html', context)


@login_required(login_url='signin')
def editservicedetails(request, id):
    data = ServicesDetail.objects.get(id=id)
    form = ServiceDetailForm(request.POST or None, request.FILES or None, instance=data)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Tabs edited successfully!")
            return redirect('servicedetailadmin')
    context = {
        'form': form,
        'data': data
    }
    return render(request, 'admin_editServiceDetail.html', context)


@login_required(login_url='signin')
def delservicedetails(request, id):
    data = ServicesDetail.objects.get(id=id)
    data.delete()
    messages.add_message(request, messages.ERROR, "Tabs deleted successfully!")
    return redirect('servicedetailadmin')


@login_required(login_url='signin')
def adminprojects(request):
    data = Projects.objects.all()
    context = {
        'data': data
    }
    return render(request, 'admin_projects.html', context)


@login_required(login_url='signin')
def addprojects(request):
    if request.method == 'POST':
        client = request.POST['client']
        location = request.POST['location']
        nature = request.POST['nature']
        contractno = request.POST['contractno']
        valueofwork = request.POST['valueofwork']
        period = request.POST['period']
        startdate = request.POST['startdate']
        enddate = request.POST['enddate']
        percent = request.POST['percent']
        iscompleted = request.POST['iscompleted']
        completedwork = request.POST['completedwork']
        balance = request.POST['balance']
        try:
            coverimg = request.FILES['coverimg']
        except MultiValueDictKeyError:
            coverimg = None
        project = Projects(client=client, location=location, nature_of_work=nature, contract_number=contractno,
                           value_of_work=valueofwork, value_of_completed_work=completedwork, contract_period=period,
                           date_of_start=startdate, date_of_complete=enddate, percentage_of_complete=percent,
                           balance_value=balance, is_completed=iscompleted, cover_image=coverimg)
        project.save()
        messages.add_message(request, messages.SUCCESS, "Project added successfully!")
        return redirect('adminprojects')
    return render(request, 'admin_addprojects.html')


@login_required(login_url='signin')
def editproject(request, id):
    data = Projects.objects.get(id=id)
    images = ProjectsPictures.objects.filter(project_id=id)
    startdate = data.date_of_start.strftime('%Y-%m-%d')
    enddate = data.date_of_complete.strftime('%Y-%m-%d')
    defaulturl = data.cover_image
    if request.method == 'POST':
        client = request.POST['client']
        location = request.POST['location']
        nature = request.POST['nature']
        contractno = request.POST['contractno']
        valueofwork = request.POST['valueofwork']
        period = request.POST['period']
        startdate = request.POST['startdate']
        enddate = request.POST['enddate']
        percent = request.POST['percent']
        iscompleted = request.POST['iscompleted']
        completedwork = request.POST['completedwork']
        balance = request.POST['balance']
        try:
            coverimg = request.FILES['coverimg']
        except MultiValueDictKeyError:
            coverimg = data.cover_image

        data.client = client
        data.location = location
        data.nature_of_work = nature
        data.contract_number = contractno
        data.value_of_work = valueofwork
        data.contract_period = period
        data.date_of_start = startdate
        data.date_of_complete = enddate
        data.percentage_of_complete = percent
        data.is_completed = iscompleted
        data.value_of_completed_work = completedwork
        data.balance_value = balance
        if coverimg:
            data.cover_image.delete()
            data.cover_image = coverimg
        data.save()
        messages.add_message(request, messages.SUCCESS, "Project edited successfully!")
        return redirect('adminprojects')
    context = {
        'images': images,
        'data': data,
        'start': startdate,
        'end': enddate
    }
    return render(request, 'admin_editProjects.html', context)


@login_required(login_url='signin')
def delproject(request, id):
    data = Projects.objects.get(id=id)
    data1 = ProjectsPictures.objects.filter(project_id=id)
    if data1:
        for i in data1:
            i.image.delete()
    data.delete()
    messages.add_message(request, messages.ERROR, "Project deleted successfully!")
    return redirect('adminprojects')


@login_required(login_url='signin')
def addprojectimage(request):
    data = Projects.objects.all()
    context = {
        'data': data
    }
    if request.method == 'POST':
        length = request.POST.get('length')
        project = request.POST.get('project')
        projects = Projects.objects.get(id=int(project))

        for file_num in range(0, int(length)):
            ProjectsPictures.objects.create(
                project=projects,
                image=request.FILES.get(f'images{file_num}')
            )
        messages.add_message(request, messages.SUCCESS, "Images added successfully!")

    return render(request, 'admin_addprojectimage.html', context)


@login_required(login_url='signin')
def delprojectimages(request, id):
    data = ProjectsPictures.objects.get(id=id)
    id1 = data.project.id
    data.delete()
    messages.add_message(request, messages.ERROR, "Image deleted successfully!")
    return redirect('/admin/edit-project/' + str(id1))


@login_required(login_url='signin')
def contacts(request):
    contact1 = ContactDetails.objects.filter(is_responded=False)
    contact2 = ContactDetails.objects.filter(is_responded=True)
    context = {
        'contacts': contact1,
        'responded': contact2
    }
    if request.method == 'POST':
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        respondie = ContactDetails.objects.get(email=email)

        emailcontext = {
            'fname': respondie.fname,
            'lname': respondie.lname,
            'email': email,
            'phone': respondie.phone,
            'subject': subject,
            'message': message
        }

        emailtouser(emailcontext)

        respondie.respmessage = message
        respondie.is_responded = True
        respondie.save()

        return HttpResponse('200')
    return render(request, "admin_contacts.html", context)


@login_required(login_url='signin')
def quotations(request):
    quotations1 = QuotationRequest.objects.filter(is_responded=False)
    quotations2 = QuotationRequest.objects.filter(is_responded=True)
    context = {
        'quotations': quotations1,
        'responded': quotations2
    }
    if request.method == 'POST':
        email = request.POST.get('email')
        respondie = QuotationRequest.objects.get(email=email)

        subject = request.POST.get('subject')
        message = request.POST.get('message')

        emailcontext = {
            'fname': respondie.fname,
            'lname': respondie.lname,
            'email': email,
            'phone': respondie.phone,
            'subject': subject,
            'message': message
        }

        emailtouser(emailcontext)

        respondie.respmessage = message
        respondie.is_responded = True
        respondie.save()

        return HttpResponse('200')
    return render(request, "admin_quotations.html", context)


@login_required(login_url='signin')
def delcontacts(request, id):
    contact = ContactDetails.objects.get(id=id)
    contact.delete()
    messages.add_message(request, messages.ERROR, "Contact data removed successfully")
    return redirect('admincontacts')


@login_required(login_url='signin')
def delquotations(request, id):
    quotation = QuotationRequest.objects.get(id=id)
    quotation.delete()
    messages.add_message(request, messages.ERROR, "Quotation request data removed successfully")
    return redirect('adminquotations')


def emailtouser(context):
    # send mail template
    emailsubject = context["subject"]
    emailmessage = context["message"]
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


@login_required(login_url='signin')
def teams(request):
    categorydata = StaffCategory.objects.all()
    subcategorydata = StaffSubCategory.objects.all()
    teams = TeamMembers.objects.all()
    teamsform = TeamMembersForms(request.POST or None, request.FILES or None)
    categoryform = StaffCategoryForm(request.POST or None)
    subcategoryform = StaffSubCategoryForm(request.POST or None)
    if request.method == 'POST':
        type = request.POST['type']
        if type == 'category':
            if categoryform.is_valid():
                categoryform.save()
                messages.add_message(request, messages.SUCCESS, "Category added successfully!")
                return redirect('adminteams')
        elif type == 'subcategory':
            if subcategoryform.is_valid():
                subcategoryform.save()
                messages.add_message(request, messages.SUCCESS, "Sub category added successfully!")
                return redirect('adminteams')
        elif type == 'team':
            if teamsform.is_valid():
                teamsform.save()
                messages.add_message(request, messages.SUCCESS, "Team Member added successfully!")
                return redirect('adminteams')
            else:
                messages.add_message(request, messages.ERROR, "Error while adding Team Member!")
                return redirect('adminteams')

    context = {
        'categoryform': categoryform,
        'subcategoryform': subcategoryform,
        'teamsform': teamsform,
        'category': categorydata,
        'subcategory': subcategorydata,
        'teams': teams
    }
    return render(request, "admin_teams.html", context)


@login_required(login_url='signin')
def editTeamContents(request, id):
    if request.method == 'POST':
        type = request.POST['type']
        if type == 'category':
            category = request.POST['category']
            data = StaffCategory.objects.get(id=id)
            data.category = category
            data.save()
            messages.add_message(request, messages.SUCCESS, "Category edited successfully")
            return redirect('adminteams')
        elif type == 'subcategory':
            category = request.POST['category']
            subcategory = request.POST['subcategory']
            data = StaffSubCategory.objects.get(id=id)
            data.category = StaffCategory.objects.get(id=category)
            data.subcategory = subcategory
            data.save()
            messages.add_message(request, messages.SUCCESS, "Subcategory edited successfully")
            return redirect('adminteams')
        elif type == 'team':
            category = request.POST['category']
            subcategory = request.POST['subcategory']
            name = request.POST['name']
            qualification = request.POST['qualification']
            experience = request.POST['experience']
            data = TeamMembers.objects.get(id=id)
            try:
                image = request.FILES['image']
            except MultiValueDictKeyError:
                image = data.image
            data.category = StaffCategory.objects.get(id=category)
            data.subcategory = StaffSubCategory.objects.get(id=subcategory)
            data.name = name
            data.qualification = qualification
            data.experience = experience
            if image:
                data.image = image
            data.save()
            messages.add_message(request, messages.SUCCESS, "Team member edited successfully")
            return redirect('adminteams')




@login_required(login_url='signin')
def deleteCategory(request, id):
    team = StaffCategory.objects.get(id=id)
    team.delete()
    return redirect('adminteams')


@login_required(login_url='signin')
def deleteSubCategory(request, id):
    team = StaffSubCategory.objects.get(id=id)
    team.delete()
    return redirect('adminteams')


@login_required(login_url='signin')
def deleteTeamMember(request, id):
    team = TeamMembers.objects.get(id=id)
    team.delete()
    return redirect('adminteams')
