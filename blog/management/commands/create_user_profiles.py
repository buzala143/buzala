from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import UserProfile

class Command(BaseCommand):
    help = 'Creates UserProfile objects for users that don\'t have one'

    def handle(self, *args, **options):
        users_without_profile = User.objects.filter(profile__isnull=True)
        for user in users_without_profile:
            UserProfile.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Created profile for user: {user.username}'))
        
        self.stdout.write(self.style.SUCCESS(f'Created {users_without_profile.count()} user profiles'))
