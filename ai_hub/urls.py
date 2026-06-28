"""
URL configuration for ai_hub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('case-studies/', views.case_studies, name='case_studies'),
    path('reviews/', views.reviews, name='reviews'),
    path('reviews/submit/', views.submit_review, name='submit_review'),
    path('blog/', views.blog, name='blog'),
    path('blog/create/', views.create_blog, name='create_blog'),
    path('gallery/', views.gallery, name='gallery'),
    path('events/', views.events, name='events'),
    path('assistant/', views.assistant, name='assistant'),
    path('assistant/ask/', views.assistant_answer, name='assistant_answer'),
    path('contact/', views.contact, name='contact'),
    path('admin-panel/login/', views.custom_admin_login, name='custom_admin_login'),
    path('admin-panel/logout/', views.custom_admin_logout, name='custom_admin_logout'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/analytics/', views.admin_analytics, name='admin_analytics'),
    path('admin-panel/inquiries/', views.manage_inquiries, name='manage_inquiries'),
    path('admin-panel/inquiries/<int:inquiry_id>/responded/', views.mark_inquiry_responded, name='mark_inquiry_responded'),
    path('admin-panel/inquiries/<int:inquiry_id>/delete/', views.delete_inquiry, name='delete_inquiry'),
    path('admin-panel/content/', views.manage_content, name='manage_content'),
    path('admin-panel/content/<str:content_type>/', views.content_items, name='content_items'),
    path('admin-panel/content/<str:content_type>/add/', views.content_form, name='add_content_item'),
    path('admin-panel/content/<str:content_type>/<int:object_id>/edit/', views.content_form, name='edit_content_item'),
    path('admin-panel/content/<str:content_type>/<int:object_id>/delete/', views.delete_content_item, name='delete_content_item'),
    path('admin-panel/reviews/<int:review_id>/approve/', views.approve_review, name='approve_review'),
    path('admin-panel/reviews/<int:review_id>/decline/', views.decline_review, name='decline_review'),
    path('admin-panel/users/', views.user_access, name='user_access'),
    path('admin-panel/users/<int:user_id>/delete/', views.delete_admin_user, name='delete_admin_user'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
