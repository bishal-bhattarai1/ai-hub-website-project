import json
import os
import re

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import (
    AdminUserCreationForm,
    ArticleForm,
    CaseStudyForm,
    ContactRequestForm,
    CustomerReviewForm,
    EventForm,
    GalleryImageForm,
    PublicCustomerReviewForm,
    ServiceForm,
)
from .models import Article, CaseStudy, ContactRequest, CustomerReview, Event, GalleryImage, Service


def is_admin_user(user):
    return user.is_authenticated and user.is_staff


admin_required = user_passes_test(is_admin_user, login_url='custom_admin_login')


CONTENT_CONFIG = {
    'services': {
        'label': 'Services',
        'model': Service,
        'form': ServiceForm,
        'fields': ['title', 'description', 'is_active'],
    },
    'articles': {
        'label': 'Articles',
        'model': Article,
        'form': ArticleForm,
        'fields': ['title', 'summary', 'is_published', 'published_at'],
    },
    'case_studies': {
        'label': 'Case Studies',
        'model': CaseStudy,
        'form': CaseStudyForm,
        'fields': ['title', 'summary', 'content'],
    },
    'events': {
        'label': 'Events',
        'model': Event,
        'form': EventForm,
        'fields': ['title', 'event_date', 'location', 'is_active'],
    },
    'gallery': {
        'label': 'Gallery Images',
        'model': GalleryImage,
        'form': GalleryImageForm,
        'fields': ['title', 'caption', 'is_active'],
    },
    'reviews': {
        'label': 'Customer Reviews',
        'model': CustomerReview,
        'form': CustomerReviewForm,
        'fields': ['customer_name', 'company', 'review', 'rating', 'status', 'is_active'],
    },
}


def home(request):
    services_list = Service.objects.filter(is_active=True)[:3]
    articles = Article.objects.filter(is_published=True)[:3]
    reviews_list = CustomerReview.objects.filter(is_active=True)[:3]
    return render(request, 'home/index.html', {
        'services': services_list,
        'articles': articles,
        'reviews': reviews_list,
        'stats': {
            'services': Service.objects.filter(is_active=True).count(),
            'articles': Article.objects.filter(is_published=True).count(),
            'events': Event.objects.filter(is_active=True).count(),
        },
    })


def services(request):
    services_list = Service.objects.filter(is_active=True)
    fallback_services = [
        {
            'title': 'AI Consulting',
            'description': 'Opportunity discovery, feasibility reviews, model selection, and delivery planning.',
        },
        {
            'title': 'Process Automation',
            'description': 'Automate repetitive workflows across documents, email, reporting, and operations.',
        },
        {
            'title': 'Custom Chatbots',
            'description': 'Website, support, and internal assistants trained around your business knowledge.',
        },
        {
            'title': 'Data Intelligence',
            'description': 'Dashboards, predictive insights, and decision-support tools for everyday teams.',
        },
    ]
    return render(request, 'home/services.html', {
        'services': services_list,
        'fallback_services': fallback_services,
    })


def case_studies(request):
    studies = CaseStudy.objects.filter(is_active=True)
    return render(request, 'home/case_studies.html', {
        'case_studies': studies,
    })


def reviews(request):
    reviews_list = CustomerReview.objects.filter(
        is_active=True,
        status=CustomerReview.STATUS_APPROVED,
    )[:6]
    return render(request, 'home/reviews.html', {
        'reviews': reviews_list,
    })


def submit_review(request):
    if request.method == 'POST':
        form = PublicCustomerReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.status = CustomerReview.STATUS_PENDING
            review.is_active = False
            review.save()
            messages.success(request, 'Thank you for sharing your review. It will appear after admin approval.')
            return redirect('reviews')
    else:
        form = PublicCustomerReviewForm()

    return render(request, 'home/submit_review.html', {
        'review_form': form,
    })


def blog(request):
    articles = Article.objects.filter(is_published=True)
    return render(request, 'home/blog.html', {'articles': articles})


@admin_required
def create_blog(request):
    return redirect('add_content_item', content_type='articles')


def gallery(request):
    images = GalleryImage.objects.filter(is_active=True)
    return render(request, 'home/gallery.html', {'images': images})


def events(request):
    today = timezone.localdate()
    upcoming_events = Event.objects.filter(is_active=True, event_date__gte=today).order_by('event_date')
    past_events = Event.objects.filter(is_active=True, event_date__lt=today).order_by('-event_date')
    events_list = list(upcoming_events) + list(past_events)
    return render(request, 'home/events.html', {
        'events': events_list,
        'upcoming_count': upcoming_events.count(),
        'past_count': past_events.count(),
    })


def assistant(request):
    return render(request, 'home/assistant.html')


def compact_text(value, limit=700):
    text = ' '.join((value or '').split())
    if len(text) <= limit:
        return text
    return f'{text[:limit].rsplit(" ", 1)[0]}...'


def format_context_block(title, lines):
    if not lines:
        return ''
    return '\n'.join([f'{title}:', *lines])


def build_assistant_context():
    services = Service.objects.filter(is_active=True).values_list('title', 'description')[:8]
    service_lines = [
        f'- {title}: {compact_text(description)}'
        for title, description in services
    ]
    if not service_lines:
        service_lines = [
            '- AI Consulting: Opportunity discovery, feasibility reviews, model selection, and delivery planning.',
            '- Process Automation: Automate repetitive workflows across documents, email, reporting, and operations.',
            '- Custom Chatbots: Website, support, and internal assistants trained around business knowledge.',
            '- Data Intelligence: Dashboards, predictive insights, and decision-support tools for everyday teams.',
        ]

    articles = Article.objects.filter(is_published=True).values(
        'title',
        'summary',
        'content',
        'published_at',
    )[:6]
    article_lines = [
        (
            f'- {article["title"]}'
            f'{f" ({article["published_at"]})" if article["published_at"] else ""}: '
            f'{compact_text(article["summary"] or article["content"])}'
        )
        for article in articles
    ]

    events = Event.objects.filter(is_active=True).values(
        'title',
        'description',
        'event_date',
        'location',
    )[:6]
    event_lines = [
        (
            f'- {event["title"]} on {event["event_date"]}'
            f'{f" at {event["location"]}" if event["location"] else ""}: '
            f'{compact_text(event["description"])}'
        )
        for event in events
    ]

    reviews = CustomerReview.objects.filter(
        is_active=True,
        status=CustomerReview.STATUS_APPROVED,
    ).values(
        'customer_name',
        'company',
        'review',
        'rating',
    )[:6]
    review_lines = [
        (
            f'- {review["customer_name"]}'
            f'{f" from {review["company"]}" if review["company"] else ""} '
            f'({review["rating"]}/5): {compact_text(review["review"], limit=350)}'
        )
        for review in reviews
    ]

    gallery = GalleryImage.objects.filter(is_active=True).values('title', 'caption')[:6]
    gallery_lines = [
        f'- {image["title"]}: {compact_text(image["caption"], limit=300)}'
        for image in gallery
        if image['caption']
    ]

    return '\n\n'.join(filter(None, [
        'AI Hub helps clients with practical AI services.',
        format_context_block('Services', service_lines),
        format_context_block('Published articles', article_lines),
        format_context_block('Upcoming or active events', event_lines),
        format_context_block('Customer reviews', review_lines),
        format_context_block('Gallery notes', gallery_lines),
        'Contact email: aihub@gmail.com\nPhone: +977 98011101011',
        'Hours: Monday to Friday, 9:00 AM - 5:00 PM',
    ]))


def get_assistant_context():
    cache_key = 'assistant_context'
    context = cache.get(cache_key)
    if context is None:
        context = build_assistant_context()
        cache.set(
            cache_key,
            context,
            getattr(settings, 'ASSISTANT_CONTEXT_CACHE_SECONDS', 300),
        )
    return context


ASSISTANT_FAQS = [
    {
        'questions': [
            'what services do you provide',
            'what do you do',
            'what can ai hub help with',
        ],
        'answer': (
            'AI Hub helps with AI consulting, workflow automation, custom chatbots, '
            'data intelligence, and practical AI training for teams.'
        ),
    },
    {
        'questions': [
            'do you build chatbots',
            'can you create a chatbot',
            'can you make virtual assistant',
        ],
        'answer': (
            'Yes. AI Hub builds custom chatbots and virtual assistants for websites, '
            'support teams, internal knowledge, FAQs, and business workflows.'
        ),
    },
    {
        'questions': [
            'how can i contact you',
            'contact details',
            'what is your email',
            'what is your phone number',
        ],
        'answer': 'You can contact AI Hub at aihub@gmail.com or call +977 98011101011.',
    },
    {
        'questions': [
            'what are your hours',
            'when are you open',
            'working hours',
            'business hours',
        ],
        'answer': 'AI Hub is available Monday to Friday, 9:00 AM - 5:00 PM.',
    },
    {
        'questions': [
            'how much does it cost',
            'what is the price',
            'pricing',
            'cost',
        ],
        'answer': (
            'Pricing depends on the project scope, timeline, and required integrations. '
            'Please contact AI Hub with your requirements for a proper estimate.'
        ),
    },
    {
        'questions': [
            'do you offer training',
            'can you train our team',
            'ai training',
            'workshops',
        ],
        'answer': (
            'Yes. AI Hub offers practical AI training, workshops, adoption roadmaps, '
            'and responsible AI guidance for teams.'
        ),
    },
    {
        'questions': [
            'how do we start',
            'how to get started',
            'what is the next step',
            'next steps',
        ],
        'answer': (
            'Start by sharing your goals, workflow, and main pain points through the contact form. '
            'AI Hub can then recommend the right service or project path.'
        ),
    },
]


def normalize_assistant_question(value):
    return re.sub(r'[^a-z0-9 ]+', '', value.lower()).strip()


def get_quick_assistant_answer(question):
    normalized_question = normalize_assistant_question(question)
    for faq in ASSISTANT_FAQS:
        for phrase in faq['questions']:
            if phrase in normalized_question:
                return faq['answer']
    return ''


@require_POST
def assistant_answer(request):
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Please send a valid question.'}, status=400)

    question = payload.get('question', '').strip()
    if not question:
        return JsonResponse({'error': 'Please type a question first.'}, status=400)

    quick_answer = get_quick_assistant_answer(question)
    if quick_answer:
        return JsonResponse({'answer': quick_answer})

    if not os.environ.get('OPENAI_API_KEY'):
        return JsonResponse({
            'error': 'AI assistant is temporarily unavailable. Please contact support to enable this feature.',
        }, status=503)

    try:
        from openai import OpenAI

        client = OpenAI(timeout=getattr(settings, 'OPENAI_TIMEOUT', 20))
        response = client.responses.create(
            model=getattr(settings, 'OPENAI_MODEL', 'gpt-4.1-mini'),
            max_output_tokens=getattr(settings, 'OPENAI_MAX_OUTPUT_TOKENS', 220),
            instructions=(
                'You are the AI Hub website assistant. Answer client questions clearly and briefly. '
                'Keep replies under 80 words unless the client explicitly asks for detail. '
                'Use only the provided AI Hub context as your business knowledge. You may summarize, '
                'compare, and recommend services from that context. If a question needs information not '
                'included in the context, project-specific pricing, private data, or a human decision, '
                'say that AI Hub should be contacted directly. Do not invent policies, prices, dates, '
                'case studies, or guarantees.'
            ),
            input=f'{get_assistant_context()}\n\nClient question: {question}',
        )
    except ImportError:
        return JsonResponse({
            'error': 'OpenAI SDK is not installed. Run pip install -r requirements.txt.',
        }, status=503)
    except Exception:
        return JsonResponse({
            'error': 'Please choose below given options or contact our support team.',
        }, status=502)

    answer = response.output_text.strip()
    return JsonResponse({'answer': answer})


def contact(request):
    if request.method == 'POST':
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your request has been saved. We will contact you soon.')
            return redirect('contact')
    else:
        form = ContactRequestForm()

    return render(request, 'home/contact.html', {'form': form})


def custom_admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_panel')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect(request.GET.get('next') or 'admin_panel')

        messages.error(request, 'Invalid admin username or password.')

    return render(request, 'home/admin_login.html')


def custom_admin_logout(request):
    logout(request)
    return redirect('custom_admin_login')


@admin_required
def admin_panel(request):
    today = timezone.localdate()
    week_start = today - timezone.timedelta(days=6)
    inquiries = ContactRequest.objects.all()
    total_inquiries = inquiries.count()
    new_inquiries = inquiries.filter(status=ContactRequest.STATUS_NEW).count()
    responded_inquiries = inquiries.filter(status=ContactRequest.STATUS_RESPONDED).count()
    response_rate = round((responded_inquiries / total_inquiries) * 100) if total_inquiries else 0
    content_counts = {
        'services': Service.objects.count(),
        'articles': Article.objects.count(),
        'case_studies': CaseStudy.objects.count(),
        'events': Event.objects.count(),
        'gallery': GalleryImage.objects.count(),
        'reviews': CustomerReview.objects.count(),
    }
    context = {
        'total_inquiries': total_inquiries,
        'new_inquiries': new_inquiries,
        'responded_inquiries': responded_inquiries,
        'response_rate': response_rate,
        'today_inquiries': inquiries.filter(created_at__date=today).count(),
        'week_inquiries': inquiries.filter(created_at__date__gte=week_start).count(),
        'recent_inquiries': inquiries[:5],
        'recent_articles': Article.objects.order_by('-created_at')[:5],
        'content_counts': content_counts,
        'total_content': sum(content_counts.values()),
        'pending_reviews': CustomerReview.objects.filter(status=CustomerReview.STATUS_PENDING).count(),
    }
    return render(request, 'home/admin_panel.html', context)


@admin_required
def admin_analytics(request):
    today = timezone.localdate()
    week_start = today - timezone.timedelta(days=6)
    inquiries = ContactRequest.objects.all()
    total_inquiries = inquiries.count()
    new_inquiries = inquiries.filter(status=ContactRequest.STATUS_NEW).count()
    responded_inquiries = inquiries.filter(status=ContactRequest.STATUS_RESPONDED).count()
    response_rate = round((responded_inquiries / total_inquiries) * 100) if total_inquiries else 0

    inquiry_chart = []
    for offset in range(7):
        day = week_start + timezone.timedelta(days=offset)
        inquiry_chart.append({
            'label': day.strftime('%a'),
            'value': inquiries.filter(created_at__date=day).count(),
        })

    content_counts = [
        {'label': 'Services', 'value': Service.objects.count()},
        {'label': 'Blogs', 'value': Article.objects.count()},
        {'label': 'Case Studies', 'value': CaseStudy.objects.count()},
        {'label': 'Events', 'value': Event.objects.count()},
        {'label': 'Gallery', 'value': GalleryImage.objects.count()},
        {'label': 'Reviews', 'value': CustomerReview.objects.count()},
    ]
    review_status = [
        {
            'label': 'Approved',
            'value': CustomerReview.objects.filter(status=CustomerReview.STATUS_APPROVED).count(),
        },
        {
            'label': 'Pending',
            'value': CustomerReview.objects.filter(status=CustomerReview.STATUS_PENDING).count(),
        },
    ]
    total_content = sum(item['value'] for item in content_counts)

    context = {
        'total_inquiries': total_inquiries,
        'new_inquiries': new_inquiries,
        'responded_inquiries': responded_inquiries,
        'response_rate': response_rate,
        'week_inquiries': inquiries.filter(created_at__date__gte=week_start).count(),
        'total_content': total_content,
        'content_ratio_total': total_content or 1,
        'published_articles': Article.objects.filter(is_published=True).count(),
        'active_case_studies': CaseStudy.objects.filter(is_active=True).count(),
        'active_events': Event.objects.filter(is_active=True).count(),
        'inquiry_chart': inquiry_chart,
        'content_counts': content_counts,
        'review_status': review_status,
    }
    return render(request, 'home/admin_analytics.html', context)


@admin_required
def manage_inquiries(request):
    query = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()
    inquiries = ContactRequest.objects.all()

    if query:
        inquiries = inquiries.filter(
            Q(name__icontains=query)
            | Q(email__icontains=query)
            | Q(phone__icontains=query)
            | Q(company__icontains=query)
            | Q(country__icontains=query)
            | Q(job_title__icontains=query)
            | Q(job_details__icontains=query)
        )

    if status in {ContactRequest.STATUS_NEW, ContactRequest.STATUS_RESPONDED}:
        inquiries = inquiries.filter(status=status)

    stats = ContactRequest.objects.values('status').annotate(total=Count('id'))
    return render(request, 'home/manage_inquiries.html', {
        'inquiries': inquiries,
        'query': query,
        'status': status,
        'stats': {item['status']: item['total'] for item in stats},
    })


@admin_required
def mark_inquiry_responded(request, inquiry_id):
    if request.method == 'POST':
        ContactRequest.objects.filter(id=inquiry_id).update(
            status=ContactRequest.STATUS_RESPONDED,
            responded_at=timezone.now(),
        )
        messages.success(request, 'Inquiry marked as responded.')
    return redirect('manage_inquiries')


@admin_required
def delete_inquiry(request, inquiry_id):
    if request.method == 'POST':
        ContactRequest.objects.filter(id=inquiry_id).delete()
        messages.success(request, 'Inquiry deleted.')
    return redirect('manage_inquiries')


@admin_required
def manage_content(request):
    sections = []
    for key, config in CONTENT_CONFIG.items():
        sections.append({
            'key': key,
            'label': config['label'],
            'count': config['model'].objects.count(),
            'items': config['model'].objects.all()[:5],
        })
    return render(request, 'home/manage_content.html', {'sections': sections})


@admin_required
def content_items(request, content_type):
    config = CONTENT_CONFIG.get(content_type)
    if not config:
        return redirect('manage_content')

    query = request.GET.get('q', '').strip()
    items = config['model'].objects.all()
    if query:
        filters = Q()
        for field in config['fields']:
            model_field = config['model']._meta.get_field(field)
            if model_field.get_internal_type() in {'CharField', 'TextField', 'EmailField', 'URLField'}:
                filters |= Q(**{f'{field}__icontains': query})
        if filters:
            items = items.filter(filters)

    return render(request, 'home/content_items.html', {
        'content_type': content_type,
        'config': config,
        'items': items,
        'query': query,
    })


@admin_required
def content_form(request, content_type, object_id=None):
    config = CONTENT_CONFIG.get(content_type)
    if not config:
        return redirect('manage_content')

    instance = None
    if object_id:
        instance = get_object_or_404(config['model'], id=object_id)

    if request.method == 'POST':
        form = config['form'](request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, f'{config["label"]} item saved.')
            return redirect('content_items', content_type=content_type)
    else:
        form = config['form'](instance=instance)

    return render(request, 'home/content_form.html', {
        'content_type': content_type,
        'config': config,
        'form': form,
        'instance': instance,
    })


@admin_required
def delete_content_item(request, content_type, object_id):
    config = CONTENT_CONFIG.get(content_type)
    if not config:
        return redirect('manage_content')

    item = get_object_or_404(config['model'], id=object_id)
    if request.method == 'POST':
        item.delete()
        messages.success(request, f'{config["label"]} item deleted.')
    return redirect('content_items', content_type=content_type)


@admin_required
def approve_review(request, review_id):
    if request.method == 'POST':
        CustomerReview.objects.filter(id=review_id).update(
            status=CustomerReview.STATUS_APPROVED,
            is_active=True,
        )
        messages.success(request, 'Review approved and published.')
    return redirect('content_items', content_type='reviews')


@admin_required
def decline_review(request, review_id):
    if request.method == 'POST':
        CustomerReview.objects.filter(id=review_id).delete()
        messages.success(request, 'Review declined and removed.')
    return redirect('content_items', content_type='reviews')


@admin_required
def user_access(request):
    User = get_user_model()
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Admin user created.')
            return redirect('user_access')
    else:
        form = AdminUserCreationForm()

    return render(request, 'home/user_access.html', {
        'form': form,
        'users': User.objects.order_by('username'),
    })
