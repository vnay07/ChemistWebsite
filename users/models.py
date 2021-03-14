from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils.translation import ugettext_lazy as _ 
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.db.models.signals import post_save




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile-pics')
    address = models.TextField(blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^[6-9][0-9]{9}$', message="Phone number must be 10 digit number only, number should not start with 1, 2, 3, 4,or 5.")
    phone_number = models.CharField(validators=[phone_regex], max_length=10, blank=True, null=True)
    signup_confirmation = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.user.username} Profile'

    '''@receiver(post_save, sender=User)
    def update_profile_signal(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()'''


    
    
    '''def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height>300 or img.width>300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)'''

