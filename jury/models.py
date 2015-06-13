from django.db import models
from django.utils import timezone

from login.models import Profile
from uploader.models import Photo


class Rating(models.Model):
    judge = models.ForeignKey(Profile)
    photo = models.ForeignKey(Photo)
    rating = models.IntegerField()
    time = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return u"{} gave {} to {}.".format(self.judge, self.rating, self.photo)
