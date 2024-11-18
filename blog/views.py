from django.shortcuts import render, redirect, get_object_or_404,reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from .models import BlogPost, Comment, UserProfile, Testimonial
from .forms import BlogPostForm, CommentForm, ReplyForm, CustomUserCreationForm, UserProfileForm, UserRegisterForm
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from .models import BlogPost, Comment, UserProfile
from django.core.paginator import Paginator
from django.contrib import messages  # Add this import
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
import random


def index(request):
    context = {

    }
    return render(request, 'blog/index.html', context )

def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def admin_dashboard(request):
    blog_posts = BlogPost.objects.all().order_by('-created_at')
    
    # Add this debugging information
    print(f"Number of blog posts: {blog_posts.count()}")
    
    for post in blog_posts:
        post.detail_url = reverse('post_detail', args=[post.id])
    
    # Pagination (optional)
    paginator = Paginator(blog_posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'blog_posts': page_obj,
    }
    return render(request, 'blog/admin_dashboard.html', context)

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')
    template_name = 'registration/logged_out.html'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)



def home(request):
    recent_posts = BlogPost.objects.order_by('-created_at')
    testimonial = Testimonial.objects.all()
    
    if testimonial:
        testimonial = random.choice(testimonial)  # Get a random testimonial
    else:
        testimonial = None 
    # [:5]  # Get 5 most recent posts
    return render(request, 'blog/home.html', {'recent_posts': recent_posts, 'test' :testimonial})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if not post.author_name:  # If author_name is not provided, use username
                post.author_name = request.user.username
            post.save()
            messages.success(request, 'Your post has been created successfully!')
            return redirect('post_detail', post_id=post.id)
        else:
            messages.error(request, 'There was an error in your form. Please check and try again.')
    else:
        form = BlogPostForm()
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def update_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk, author=request.user)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog/update_post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('my_blogs')
    return render(request, 'blog/delete_post.html', {'post': post})

@login_required
def post_list(request):
    posts = BlogPost.objects.filter(author=request.user)
    return render(request, 'blog/post_list.html', {'posts': posts})

@user_passes_test(is_admin)
def admin_post_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'blog/admin_post_list.html', {'posts': posts})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone_number = form.cleaned_data.get('phone_number')
            profession = form.cleaned_data.get('profession')

            UserProfile.objects.update_or_create(
                user=user,
                defaults={'phone_number': phone_number, 'profession': profession}
            )
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def test_view(request):
    return render(request, 'test.html')

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    comments = post.comments.all().order_by('-created_at')
    
    if request.method == 'POST':
        if 'comment_form' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid() and request.user.is_authenticated:
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.author = request.user
                new_comment.save()
                return redirect('post_detail', post_id=post.id)
        elif 'reply_form' in request.POST:
            reply_form = ReplyForm(request.POST)
            if reply_form.is_valid() and request.user.is_authenticated:
                comment_id = request.POST.get('comment_id')
                parent_comment = get_object_or_404(Comment, id=comment_id)
                new_reply = reply_form.save(commit=False)
                new_reply.comment = parent_comment
                new_reply.author = request.user
                new_reply.save()
                return redirect('post_detail', post_id=post.id)
    
    comment_form = CommentForm()
    reply_form = ReplyForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'reply_form': reply_form,
        
    }
    return render(request, 'blog/post_detail.html', context)

def about(request):
    return render(request, 'blog/about.html')

@login_required
def my_blogs(request):
    user_posts = BlogPost.objects.filter(author=request.user).order_by('-created_at')
    paginator = Paginator(user_posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/my_blogs.html', {'page_obj': page_obj})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id, author=request.user)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})

@csrf_exempt
def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('home')  # or whatever URL you want to redirect after logout

def privacy_policy(request):
    return render(request, 'blog/privacy_policy.html')

def terms_of_service(request):
    return render(request, 'blog/terms_of_service.html')

@user_passes_test(is_admin)
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = BlogPost.objects.filter(author=user)
    return render(request, 'blog/user_profile.html', {'profile_user': user, 'posts': posts})

@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    if request.user != user and not request.user.is_staff:
        raise PermissionDenied
    profile, created = UserProfile.objects.get_or_create(user=user)
    return render(request, 'blog/user_profile.html', {
        'profile_user': user,
        'profile': profile,
        
    })

@login_required
def edit_profile(request, username):
    user = get_object_or_404(User, username=username)
    if request.user != user and not request.user.is_staff:
        raise PermissionDenied
    
    # Get or create the user's profile
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile', username=username)
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'blog/edit_profile.html', {'form': form, 'profile_user': user})

from django.http import HttpResponseForbidden
import os

@login_required
def delete_file(request, file_id):
    file = get_object_or_404(UserFile, id=file_id)
    if file.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to delete this file.")
    
    file_path = file.file.path
    if os.path.exists(file_path):
        os.remove(file_path)
    
    file.delete()
    return redirect('user_profile', username=request.user.username)



@login_required
def unsubscribe(request):
    if request.method == 'POST':
        user = request.user
        user.is_active = False
        user.save()
        messages.success(request, "Your account has been deactivated. We're sorry to see you go!")
        logout(request)
        return redirect('home')
    return render(request, 'blog/unsubscribe.html')

def testimonial(request):

    context = {

    }
    return render(request, 'blog/testimonial.html', context)



def random_testimonial(request):
    testimonial = Testimonial.objects.all()
    
    # if testimonials:
    #     testimonial = random.choice(testimonials)  # Get a random testimonial
    # else:
    #     testimonial = None  # Handle case with no testimonials

    return render(request, 'blog/testimonial.html', {'testimonial': testimonial})

