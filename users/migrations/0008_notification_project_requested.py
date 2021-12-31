# Generated by Django 4.0 on 2021-12-31 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_alter_project_mailnotification'),
        ('users', '0007_notification_notification_from_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='project_requested',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='project_requested', to='home.project'),
            preserve_default=False,
        ),
    ]
