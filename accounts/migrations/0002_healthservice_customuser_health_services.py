# Generated by Django 4.1.7 on 2023-03-28 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HealthService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='health_services',
            field=models.ManyToManyField(related_name='health_services', to='accounts.healthservice'),
        ),
    ]
