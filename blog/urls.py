from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('caselist', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('my-blogs/', views.my_blogs, name='my_blogs'),
    path('posts/', views.post_list, name='post_list'),
    path('create/', views.create_post, name='create_post'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('update/<int:pk>/', views.update_post, name='update_post'),
    path('admin/posts/', views.admin_post_list, name='admin_post_list'),
    path('register/', views.register, name='register'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),  
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('user-profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),
    path('delete-file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
    path('testimonial/', views.random_testimonial, name = 'random_testimonial')

]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)