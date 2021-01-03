from django import forms
from LandingPage.models import ServicesDetail, HomeSlider, StaffCategory, StaffSubCategory, TeamMembers


class ServiceDetailForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title goes here...'}))
    image = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Image goes here...'}))
    descriptions = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description goes here...', 'rows': '3'}))

    class Meta:
        model = ServicesDetail
        fields = '__all__'


class HomeSliderForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title goes here...'}))
    subtitle = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subtitle goes here...'}))
    image = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Image goes here...'}))

    class Meta:
        model = HomeSlider
        fields = '__all__'


class StaffCategoryForm(forms.ModelForm):
    category = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category goes here...'}))

    class Meta:
        model = StaffCategory
        fields = '__all__'


class StaffSubCategoryForm(forms.ModelForm):
    subcategory = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sub category goes here...'}))

    class Meta:
        model = StaffSubCategory
        fields = '__all__'


class TeamMembersForms(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name goes here...'}))
    qualification = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Qualification goes here...'}))
    experience = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Experience goes here...'}))

    class Meta:
        model = TeamMembers
        fields = '__all__'
