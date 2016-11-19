import os

# from django.contrib.auth.decorators import login_required
# from django.views.decorators.cache import cache_page
from django.db.models import Sum, Count
from django.shortcuts import render

from uploader.models import Salon, Theme, Photo
from login.models import Profile as User, Institution


# @login_required
def select_results(request):
    salons = Salon.objects.all()

    response = {'salons': salons}
    return render(request, os.path.join('results', 'select_results.html'), response)


# @login_required
def select_school_results(request):
    salons = Salon.objects.all()

    resp = {'salons': salons}
    return render(request, os.path.join('results', 'select_school_results.html'), resp)


# @login_required
def photo_view(request, photo_id):
    photo = Photo.objects.get(pk=photo_id)

    response = {'photo': photo}
    return render(request, os.path.join('results', 'photo.html'), response)


# @login_required
def results(request, salon_id):
    salon = Salon.objects.filter(pk=salon_id)[0]
    theme = Theme.objects.filter(salon=salon)[0]

    photos = Photo.objects.filter(
        theme=theme
    ).annotate(
        Sum('rating__rating')
    ).order_by(
        'user__first_name',
        'user__last_name',
        'user__pk'
    )

    prev_author = None
    authors = []

    for photo in photos:
        if prev_author != photo.user.pk:
            # if len(authors) > 0:
            #     while len(authors[-1]) < 3:
            #         authors[-1].append(None)
            authors.append([])
        authors[-1].append(photo)
        prev_author = photo.user.pk

    best_author = User.objects.filter(  # pylint: disable=no-member
        photo__theme=theme
    ).annotate(
        Count('pk')
    ).annotate(
        sum=Sum('photo__rating__rating')
    ).order_by(
        '-sum'
    )[0].pk

    gold, silver, bronze, accepted, hms = 0, 0, 0, 0, []

    if salon_id == '1':  # TODO
        gold = 993
        silver = 292
        bronze = 679
        hms = [256, 389, 822]
        accepted = 13

    if salon_id == '2':
        gold = 5
        silver = 916
        bronze = 57
        hms = [588, 969, 158, 1011]
        accepted = 16

    response = {'authors': authors, 'best_author': best_author, 'salon': salon,
                'gold': gold, 'silver': silver, 'bronze': bronze, 'hms': hms,
                'accepted': accepted}
    return render(request, os.path.join('results', 'results.html'), response)


# @login_required
def school_results(request, salon_id):
    salon = Salon.objects.filter(pk=salon_id)[0]
    theme = Theme.objects.filter(salon=salon)[0]

    schools = []

    for school in Institution.objects.all():
        photos = Photo.objects.filter(theme=theme, user__school=school.name) \
                              .annotate(sum=Sum('rating__rating')) \
                              .order_by('-sum')

        if len(photos) > 10:
            photos = photos[:10]

        rating = sum([p.sum for p in photos])
        if rating > 0:
            schools.append({'name': school.name, 'rating': rating})

        schools = sorted(schools, key=lambda school: school['rating'], reverse=True)

    response = {'schools': schools, 'salon': salon}
    return render(request, os.path.join('results', 'school_results.html'), response)
