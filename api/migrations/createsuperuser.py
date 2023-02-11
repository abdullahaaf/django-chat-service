from decouple import config
from django.db import migrations
from django.utils import timezone

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_rename_user_2_chatrooms_receiver_and_more'),
    ]

    def generate_superuser(apps, schema_editor):
        from django.contrib.auth.models import User

        DJANGO_SU_NAME = config('SUUSERNAME')
        DJANGO_SU_EMAIL = config('SUEMAIL')
        DJANGO_SU_PASSWORD = config('SUPASSWORD')
        DJANGO_FIRST_NAME = config('FIRST_NAME')
        DJANGO_LAST_NAME = config('LAST_NAME')

        superuser = User.objects.create_superuser(
            username=DJANGO_SU_NAME,
            first_name=DJANGO_FIRST_NAME,
            last_name=DJANGO_LAST_NAME,
            is_superuser=True,
            is_staff=True,
            is_active=True,
            email=DJANGO_SU_EMAIL,
            password=DJANGO_SU_PASSWORD,
            last_login=timezone.now())

        superuser.save()

    operations = [
        migrations.RunPython(generate_superuser),
    ]