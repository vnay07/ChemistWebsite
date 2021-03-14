# Generated by Django 3.0.2 on 2021-02-20 09:33

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpg', upload_to='profile-pics')),
                ('address', models.TextField(blank=True, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=13, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 12 digits allowed and + sign.", regex='/^(?:(?:\\+|0{0,2})91(\\s*|[\\-])?|[0]?)?([6789]\\d{2}([ -]?)\\d{3}([ -]?)\\d{4})$/')])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]