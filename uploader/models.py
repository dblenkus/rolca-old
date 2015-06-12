import StringIO

from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings

from datetime import date
from PIL import Image


class Salon(models.Model):
    """Model for storing salons.



    """
    #: title of the salon
    title = models.CharField(max_length=100)

    #: date when salon starts
    start_date = models.DateField()

    #: date when salon ends
    end_date = models.DateField()

    #: date when judging will take place
    jury_date = models.DateField()

    #: date when results will be published
    results_date = models.DateField()

    #: list of judges
    judges = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __unicode__(self):
        """Return salon's title."""
        return self.title

    def is_active(self):
        """Check if salon is active."""
        return self.start_date <= date.today() <= self.end_date
    is_active.admin_order_field = 'end_date'
    is_active.boolean = True


class Theme(models.Model):
    """Model for storing themes.



    """

    #: title of the theme
    title = models.CharField(max_length=100)

    #: salon that theme belongs to
    salon = models.ForeignKey(Salon)

    #: number of photos that can be submited to theme
    n_photos = models.IntegerField('Number of photos')

    def __unicode__(self):
        """Return theme's title."""
        return self.title


class File(models.Model):
    """Model for storing uploaded images.

    Uploaded images can be stored prior to creating Photo instance. This
    way you can upload images while user is typing other data.
    Images are checked if meet size and format requirements before
    saving.

    """
    file = models.ImageField(upload_to='photos')
    thumbnail = models.ImageField(upload_to='thumbs')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        if not self.pk:
            fn = Image.open(self.file)
            fn.thumbnail((100, 100), Image.ANTIALIAS)
            thumb_io = StringIO.StringIO()
            fn.save(thumb_io, "JPEG", quality=100, optimize=True,
                    progressive=True)
            thumb_file = InMemoryUploadedFile(thumb_io, None, self.file.name,
                                              'image/jpeg', thumb_io.len, None)
            self.thumbnail = thumb_file

        super(File, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # pylint: disable=no-member
        self.file.delete(False)
        self.thumbnail.delete(False)
        # pylint: enable=no-member

        super(File, self).delete(*args, **kwargs)

    def longer_edge(self):
        return max(self.file.width, self.file.height)  # pylint: disable=no-member

    def __unicode__(self):
        return self.file.name


class Photo(models.Model):
    """Model for storing uploaded photos.



    """
    title = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    theme = models.ForeignKey(Theme)
    photo = models.ForeignKey(File)

    def __unicode__(self):
        return self.title
