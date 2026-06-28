from django.contrib import admin

from .models import Article, CaseStudy, ContactRequest, CustomerReview, Event, GalleryImage, Service


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'company', 'country', 'job_title', 'status', 'created_at')
    search_fields = ('name', 'email', 'company', 'country', 'job_title', 'job_details')
    list_filter = ('status', 'country', 'created_at')
    readonly_fields = ('created_at', 'responded_at')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('is_active',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'published_at', 'created_at')
    search_fields = ('title', 'summary', 'content')
    list_filter = ('is_published', 'published_at')


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    fields = ('title', 'summary', 'content')
    list_display = ('title', 'created_at')
    search_fields = ('title', 'summary', 'content')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'location', 'is_active')
    search_fields = ('title', 'description', 'location')
    list_filter = ('is_active', 'event_date')


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    search_fields = ('title', 'caption', 'image_url')
    list_filter = ('is_active',)


@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'company', 'rating', 'status', 'is_active', 'created_at')
    search_fields = ('customer_name', 'company', 'review')
    list_filter = ('status', 'rating', 'is_active', 'created_at')
