from decouple import config
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_rename_user_2_chatrooms_receiver_and_more'),
    ]

    def generate_superuser(apps, schema_editor):
        from django.contrib.auth.models import User

        DJANGO_SU_NAME = config('SUUSERNAME')
        DJANGO_SU_EMAIL = config('SUEMAIL')
        DJANGO_SU_PASSWORD = config('SUPASSWORD')

        superuser = User.objects.create_superuser(
            username=DJANGO_SU_NAME,
            email=DJANGO_SU_EMAIL,
            password=DJANGO_SU_PASSWORD)

        superuser.save()

    operations = [
        migrations.RunPython(generate_superuser),
    ]