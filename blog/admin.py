from django.contrib import admin
from .models import BlogPost, Comment, Reply, UserProfile, Testimonial
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.

admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Testimonial)


class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'is_staff', 'get_telephone')

    def get_telephone(self, instance):
        return instance.profile.phone_number
    get_telephone.short_description = 'Telephone'

    def view_on_site(self, obj):
        return f'/user-profile/{obj.id}/'

admin.site.unregister(User)
admin.site.register(User, UserAdmin)