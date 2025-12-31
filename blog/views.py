from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.core.paginator import Paginator  # Capital 'P'
from .forms import ContactForm  # ✅ import your form
import logging

logger = logging.getLogger(__name__)  # ✅ Move logger here (correct position)


def home(request):
    all_posts = Post.objects.all()  # optional ordering by newest first
    paginator = Paginator(all_posts, 6)  # Capital 'P' and 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shop/home.html', {'page_obj': page_obj})


def register(request):
    return render(request, 'shop/register.html')


def index(request, post_id):
    return HttpResponse(f"its me naveen is on {post_id}")


def headerandfooter(request):
    return render(request, 'shop/headerandfooter.html')


def postinfo(request, post_id):
    # Fetch the post by id and return a template
    post = Post.objects.get(id=post_id)
    return render(request, 'shop/postinfo.html', {'post': post})


def header(request):
    return render(request, 'shop/header.html')


def contact(request):
    success_message = ""

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            logger.debug(f"Post data is: {name}, {email}, {message}")
            success_message = "Thanks for contacting us!"
            form = ContactForm()  # Reset the form after success
    else:
        form = ContactForm()

    return render(request, 'shop/contact.html', {
        'form': form,
        'success_message': success_message
    })
    
    

def about(request):
    return render(request, 'shop/about.html')





   