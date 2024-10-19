from django.shortcuts import render, get_object_or_404
from django.http import Http404
from home.models import Blog
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.db.models import Q
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import random
import re


def is_empty(*args):
    """Проверяет, пусты ли переданные поля."""
    return any(arg.strip() == '' for arg in args)


def paginate_queryset(queryset, request, per_page=3):
    """Пагинация для переданного queryset."""
    paginator = Paginator(queryset, per_page)
    page = request.GET.get('page')
    return paginator.get_page(page)


def index(request):
    blogs = Blog.objects.all()
    random_blogs = random.sample(list(blogs), 3)
    context = {'random_blogs': random_blogs}
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')


def thanks(request):
    return render(request, 'thanks.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        if is_empty(name, email, phone, message):
            messages.error(request, 'One or more fields are empty!')
        else:
            try:
                validate_email(email)
                phone_pattern = re.compile(r'^[0-9]{10}$')

                if phone_pattern.match(phone):
                    form_data = {
                        'name': name,
                        'email': email,
                        'phone': phone,
                        'message': message,
                    }
                    message_body = f'''
                    From:\n\t\t{form_data['name']}\n
                    Message:\n\t\t{form_data['message']}\n
                    Email:\n\t\t{form_data['email']}\n
                    Phone:\n\t\t{form_data['phone']}\n
                    '''
                    send_mail('You got a mail!', message_body, '', ['dev.ash.py@gmail.com'])
                    messages.success(request, 'Your message was sent.')
                    return redirect('thanks')
                else:
                    messages.error(request, 'Phone number is invalid!')
            except ValidationError:
                messages.error(request, 'Email is invalid!')

    return render(request, 'contact.html', {})


def projects(request):
    return render(request, 'projects.html')


def blog(request):
    blogs = Blog.objects.all().order_by('-time')
    blogs = paginate_queryset(blogs, request)
    context = {'blogs': blogs}
    return render(request, 'blog.html', context)


def category(request, category):
    category_posts = Blog.objects.filter(category=category).order_by('-time')
    if not category_posts:
        message = f"No posts found in category: '{category}'"
        return render(request, "category.html", {"message": message})

    category_posts = paginate_queryset(category_posts, request)
    return render(request, "category.html", {"category": category, 'category_posts': category_posts})


def categories(request):
    all_categories = Blog.objects.values('category').distinct().order_by('category')
    return render(request, "categories.html", {'all_categories': all_categories})


def search(request):
    query = request.GET.get('q', '')
    query_list = query.split()
    filters = Q()

    for word in query_list:
        filters |= Q(title__icontains=word) | Q(content__icontains=word)

    results = Blog.objects.filter(filters).order_by('-time')
    results = paginate_queryset(results, request)

    message = "Sorry, no results found for your search query." if not results else ""
    return render(request, 'search.html', {'results': results, 'query': query, 'message': message})


def blogpost(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    return render(request, 'blogpost.html', {'blog': blog})
