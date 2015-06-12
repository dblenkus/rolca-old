from django.db import models


class Workshop(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    limit = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    instructor = models.CharField(max_length=100)

    def count(self):
        num = 0
        for application in Application.objects.filter(workshop=self):
            num += application.n_of_applicants
        return num

    def __unicode__(self):
        return u'{}'.format(self.title)


class Application(models.Model):
    workshop = models.ForeignKey(Workshop)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    institution = models.BooleanField(default=False)
    institution_name = models.CharField(max_length=100, blank=True)
    n_of_applicants = models.IntegerField()

    def __unicode__(self):
        return '{} - {}'.format(self.workshop.title, self.name)
