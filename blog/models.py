from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True)
    profession = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.profile.save()



@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # instance.userprofile.save()
    pass


class BlogPost(models.Model):
    AGAINST_CHOICES = [
        ('Eastern Cape', 'Eastern Cape'),
        ('Free State', 'Free State'),
        ('Gauteng', 'Gauteng'),
        ('KwaZulu-Natal', 'KwaZulu-Natal'),
        ('Limpopo', 'Limpopo'),
        ('Mpumalanga', 'Mpumalanga'),
        ('North West', 'North West'),
        ('Western Cape', 'Western Cape'),
        ('Northern Cape', 'Northern Cape,'),
      
    ]


    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    author_name = models.CharField(max_length=100, blank=True)  # New field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    against = models.CharField(max_length=100)
    suburb = models.CharField(max_length=100)
    incident_date = models.DateField()
    file1 = models.FileField(upload_to='blog_files/', blank=True, null=True)
    file2 = models.FileField(upload_to='blog_files/', blank=True, null=True)
    file3 = models.FileField(upload_to='blog_files/', blank=True, null=True)
    file4 = models.FileField(upload_to='blog_files/', blank=True, null=True)
    province = models.CharField(max_length=100, choices=AGAINST_CHOICES)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'


class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reply by {self.author.username} to {self.comment}'



class Testimonial(models.Model):
    author_name = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return f'Testimonial by {self.author_name}'


