from __future__ import absolute_import, division, print_function, unicode_literals

import StringIO

from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

from datetime import date
from PIL import Image


@python_2_unicode_compatible
class Salon(models.Model):
    """Model for storing salons.

    Salon object is the main object of single salon. It  can contain
    multiple themes, all important dates for salone (start, end, jury
    and results date) and list of judges.

    """
    #: user who created salon
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='salons_owned')

    #: date salon was created
    created = models.DateTimeField(auto_now_add=True)

    #: date salon was last modified
    modified = models.DateTimeField(auto_now=True)

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
    judges = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='salons_judged')

    def __str__(self):
        """Return salon's title."""
        return self.title

    def is_active(self):
        """Check if salon is active."""
        return self.start_date <= date.today() <= self.end_date
    is_active.admin_order_field = 'end_date'
    is_active.boolean = True


@python_2_unicode_compatible
class Theme(models.Model):
    """Model for storing themes.

    Theme object

    """

    #: date theme was created
    created = models.DateTimeField(auto_now_add=True)

    #: date theme was last modified
    modified = models.DateTimeField(auto_now=True)

    #: title of the theme
    title = models.CharField(max_length=100)

    #: salon that theme belongs to
    salon = models.ForeignKey(Salon, related_name='themes')

    #: number of photos that can be submited to theme
    n_photos = models.IntegerField('Number of photos')

    def __str__(self):
        """Return theme's title."""
        return self.title


@python_2_unicode_compatible
class File(models.Model):
    """Model for storing uploaded images.

    Uploaded images can be stored prior to creating Photo instance. This
    way you can upload images while user is typing other data.
    Images are checked if meet size and format requirements before
    saving.

    """

    #: date file was created
    created = models.DateTimeField(auto_now_add=True)

    #: date file was last modified
    modified = models.DateTimeField(auto_now=True)

    #: uploaded file
    file = models.ImageField(upload_to='photos')

    #: thumbnail of uploaded file
    thumbnail = models.ImageField(upload_to='thumbs')

    #: user, who uploaded file
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        if not self.pk and self.file:
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
        # delete attached files
        self.file.delete(save=False)  # pylint: disable=no-member
        self.thumbnail.delete(save=False)  # pylint: disable=no-member

        super(File, self).delete(*args, **kwargs)

    def longer_edge(self):
        return max(self.file.width, self.file.height)  # pylint: disable=no-member

    def __str__(self):
        return self.file.name


@python_2_unicode_compatible
class Participent(models.Model):
    """ Model for storing participents.


    """

    #: date participent was created
    created = models.DateTimeField(auto_now_add=True)

    #: date participent was last modified
    modified = models.DateTimeField(auto_now=True)

    #: user, wko uploaded participent's photos
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL)

    #: participent's first name
    first_name = models.CharField(max_length=30)

    #: participent's last name
    last_name = models.CharField(max_length=30)

    #: mentor
    mentor = models.CharField(max_length=30)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


@python_2_unicode_compatible
class Photo(models.Model):
    """Model for storing uploaded photos.



    """
    #: date photo was created
    created = models.DateTimeField(auto_now_add=True)

    #: date photo was last modified
    modified = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=100)

    participent = models.ForeignKey('Participent')

    theme = models.ForeignKey(Theme)

    photo = models.ForeignKey(File)

    def __str__(self):
        return self.title
