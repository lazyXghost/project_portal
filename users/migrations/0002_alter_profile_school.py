# Generated by Django 4.1.7 on 2023-03-22 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='school',
            field=models.CharField(choices=[('SBS', 'SBS'), ('SCS', 'SCS'), ('SPS', 'SPS'), ('SMSS', 'SMSS'), ('SHSS', 'SHSS'), ('SCEE', 'SCEE'), ('SMMS', 'SMMS'), ('SCENE', 'SCENE'), ('SoM', 'SoM')], max_length=100),
        ),
    ]
