from django.db import models
from django.utils import timezone


class ContactRequest(models.Model):
    STATUS_NEW = 'new'
    STATUS_RESPONDED = 'responded'
    STATUS_CHOICES = [
        (STATUS_NEW, 'New'),
        (STATUS_RESPONDED, 'Responded'),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    company = models.CharField(max_length=160)
    country = models.CharField(max_length=100)
    job_title = models.CharField(max_length=120)
    job_details = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    responded_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.company}'


class Service(models.Model):
    title = models.CharField(max_length=140)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=180)
    summary = models.TextField()
    content = models.TextField()
    published_at = models.DateField(blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title


class CaseStudy(models.Model):
    title = models.CharField(max_length=180)
    tag = models.CharField(max_length=80, default='Customer AI')
    summary = models.TextField()
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='case_studies/', blank=True, null=True)
    metric_one_value = models.CharField(max_length=40, blank=True)
    metric_one_label = models.CharField(max_length=120, blank=True)
    metric_two_value = models.CharField(max_length=40, blank=True)
    metric_two_label = models.CharField(max_length=120, blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', '-is_featured', '-created_at']

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=180)
    description = models.TextField()
    event_date = models.DateField()
    location = models.CharField(max_length=180, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['event_date']

    def __str__(self):
        return self.title

    @property
    def is_upcoming(self):
        return self.event_date >= timezone.localdate()

    @property
    def event_status_label(self):
        return 'Upcoming Session' if self.is_upcoming else 'Session Ended'

    @property
    def event_status_class(self):
        return 'upcoming' if self.is_upcoming else 'past'


class GalleryImage(models.Model):
    title = models.CharField(max_length=140)
    image = models.ImageField(upload_to='gallery/', blank=True, null=True)
    image_url = models.URLField(blank=True)
    caption = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class CustomerReview(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
    ]

    customer_name = models.CharField(max_length=140)
    company = models.CharField(max_length=160, blank=True)
    review = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_APPROVED)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.customer_name
