from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('projects/', views.projects, name="projects"),
    path('manpower/', views.manpower, name="manpower"),
    path('newsletter/', views.newsletter, name="newsletter"),
    path('contact-us/', views.contacts, name="contacts"),
    path('certificates/', views.certificate, name="certificate"),
    path('company-profile/', views.cprofile, name="cprofile"),
    path('equipments/', views.equipments, name="equipments"),
    path('check-email-contact/', views.check_email_c, name="checkemailc"),
    path('check-email-quotation/', views.check_email_q, name="checkemailq"),
    path('quotation-request/', views.quotations, name="quotations"),
    path('project/<int:id>', views.singleprojects, name="singleproject"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
