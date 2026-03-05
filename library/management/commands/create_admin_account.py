from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "初始化管理员账户"

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str)
        parser.add_argument('--email', type=str)
        parser.add_argument('--password', type=str)

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        user, created = User.objects.get_or_create(
            username=username,
            defaults={'is_staff': True, 'is_superuser': True},
        )
        if not created:
            user.is_staff = True
            user.is_superuser = True
        if email:
            user.email = email
        user.set_password(password)
        user.save()

        self.stdout.write(self.style.SUCCESS("成功初始化管理员账户"))
