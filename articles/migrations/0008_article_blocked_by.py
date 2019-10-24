# Generated by Django 2.2.5 on 2019-10-23 09:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_article_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='blocked_by',
            field=models.ManyToManyField(blank=True, related_name='blocked_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
