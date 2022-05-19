from django.db import models
from django.contrib.auth.models import User
from PIL import Image

def directory_path(instance, filename):
    return '{0}/{1}/{2}'.format(instance.__class__.__name__, str(instance.user)[0], filename)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile/default.png', upload_to=directory_path)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)




