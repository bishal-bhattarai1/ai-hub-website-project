from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Article, CaseStudy, ContactRequest, CustomerReview, Event, GalleryImage, Service


class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = [
            'name',
            'email',
            'phone',
            'company',
            'country',
            'job_title',
            'job_details',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
            'phone': forms.TextInput(attrs={'placeholder': '+1 555 000 0000'}),
            'company': forms.TextInput(attrs={'placeholder': 'Company or organization'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),
            'job_title': forms.TextInput(attrs={'placeholder': 'Your role'}),
            'job_details': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Describe the work, goals, timeline, integrations, or problems you want to solve.',
            }),
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'is_active']


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'summary', 'content', 'published_at', 'is_published']
        widgets = {
            'published_at': forms.DateInput(attrs={'type': 'date'}),
        }


class PublicArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'summary', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Blog title'}),
            'summary': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write a short summary for the blog card.',
            }),
            'content': forms.Textarea(attrs={
                'rows': 8,
                'placeholder': 'Write the full blog post here.',
            }),
        }


class CaseStudyForm(forms.ModelForm):
    class Meta:
        model = CaseStudy
        fields = ['title', 'summary', 'content']
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 3}),
            'content': forms.Textarea(attrs={'rows': 6}),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_date', 'location', 'is_active']
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
        }


class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['title', 'image', 'caption', 'is_active']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image and not self.instance.pk:
            raise forms.ValidationError('Please upload a gallery photo.')
        return image


class CustomerReviewForm(forms.ModelForm):
    class Meta:
        model = CustomerReview
        fields = ['customer_name', 'company', 'review', 'rating', 'status', 'is_active']


class PublicCustomerReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(value, f'{value} star{"s" if value != 1 else ""}') for value in range(5, 0, -1)],
        initial=5,
    )

    class Meta:
        model = CustomerReview
        fields = ['customer_name', 'company', 'review', 'rating']
        widgets = {
            'customer_name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'company': forms.TextInput(attrs={'placeholder': 'Company or organization'}),
            'review': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Share your experience with AI Hub.',
            }),
        }


class AdminUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=False)
    is_staff = forms.BooleanField(required=False, initial=True)
    is_superuser = forms.BooleanField(required=False)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email', '')
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.is_staff = self.cleaned_data.get('is_staff', True)
        user.is_superuser = self.cleaned_data.get('is_superuser', False)
        if commit:
            user.save()
        return user
