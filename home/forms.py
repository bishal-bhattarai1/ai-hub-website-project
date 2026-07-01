from django import forms
from django.contrib.auth import get_user_model

from .models import Article, CaseStudy, ContactRequest, CustomerReview, Event, GalleryImage, Service


class ContactRequestForm(forms.ModelForm):
    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if not email.endswith('@gmail.com'):
            raise forms.ValidationError('Please enter a valid Gmail address ending with @gmail.com.')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not phone.isdigit():
            raise forms.ValidationError('Phone number must contain digits only.')
        if len(phone) > 10:
            raise forms.ValidationError('Phone number cannot be more than 10 digits.')
        return phone

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
            'email': forms.EmailInput(attrs={'placeholder': 'you@gmail.com'}),
            'phone': forms.TextInput(attrs={
                'maxlength': '10',
                'placeholder': '10 digit phone number',
            }),
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
                'placeholder': 'Share your experience with AI Solution.',
            }),
        }


class AdminUserCreationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
    )
    confirm_password = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Re-enter password'}),
    )
    is_superuser = forms.BooleanField(
        label='Give full admin permissions',
        required=False,
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password', 'confirm_password', 'is_superuser']
        labels = {
            'username': 'Username',
            'email': 'Email',
        }
        help_texts = {
            'username': '',
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email address'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        User = get_user_model()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Confirm password does not match.')
        return confirm_password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email', '').strip()
        user.is_staff = True
        user.is_superuser = self.cleaned_data.get('is_superuser', False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
