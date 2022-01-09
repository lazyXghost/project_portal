# Generated by Django 4.0.1 on 2022-01-09 08:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0008_alter_project_floatedby_remove_project_mentors_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='Mentors',
        ),
        migrations.AddField(
            model_name='project',
            name='Mentors',
            field=models.ManyToManyField(default=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='FloatedBy', to=settings.AUTH_USER_MODEL), related_name='Mentors', to=settings.AUTH_USER_MODEL),
        ),
    ]
