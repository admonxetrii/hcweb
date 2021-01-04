from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

#ADMIN URL

urlpatterns = [
    path('', views.homeslideradmin, name="adminhome"),
    path('signin/', views.signin, name="signin"),
    path('signout/', views.signout, name="signout"),
    path('servicedetail/', views.servicedetailadmin, name="servicedetailadmin"),
    path('homepagecontents/', views.homepageextra, name="homepagecontents"),
    path('projects/', views.adminprojects, name="adminprojects"),
    path('teams/', views.teams, name="adminteams"),
    path('edit-teams/<int:id>', views.editTeamContents, name="admineditteams"),
    path('delete-teams/<int:id>', views.deleteTeamMember, name="deleteteams"),
    path('delete-team-category/<int:id>', views.deleteCategory, name="deletecategory"),
    path('delete-team-subcategory/<int:id>', views.deleteSubCategory, name="deletesubcategory"),
    path('contacts/', views.contacts, name="admincontacts"),
    path('quotations/', views.quotations, name="adminquotations"),
    path('del-contact/<int:id>', views.delcontacts, name="admindelcontacts"),
    path('del-quotation/<int:id>', views.delquotations, name="admindelquotations"),
    path('add-projects/', views.addprojects, name="addprojects"),
    path('add-project-image/', views.addprojectimage, name="addprojectimage"),
    path('edit-servicedetail/<int:id>', views.editservicedetails, name="editservicedetails"),
    path('edit-slider/<int:id>', views.edithomeslider, name="edithomeslider"),
    path('edit-project/<int:id>', views.editproject, name="editproject"),
    path('delete-slider/<int:id>', views.delhomeslider, name="delhomeslider"),
    path('delete-project/<int:id>', views.delproject, name="delproject"),
    path('delete-project-image/<int:id>', views.delprojectimages, name="delprojectimages"),
    path('delete-servicedetail/<int:id>', views.delservicedetails, name="delservicedetails"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
