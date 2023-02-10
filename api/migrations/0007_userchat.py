# Generated by Django 4.1.5 on 2023-02-10 01:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0006_alter_message_timestamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_message', to='api.message')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]