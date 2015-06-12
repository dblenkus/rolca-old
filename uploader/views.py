# -*- coding: utf-8 -*-
import datetime
import json
import logging
import os

from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed)
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt


from .models import File, Photo, Salon, Theme
from login.models import UserProfile


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


@login_required
def upload_app(request):
    # pylint: disable=too-many-branches
    msgs = []
    errors = []
    files = []

    if request.method == 'POST':
        print request.POST
        print request.FILES

        for i in [1, 2, 3]:
            if 'photo{}'.format(i) in request.FILES:
                photo = request.FILES['photo{}'.format(i)]
                title = request.POST['title{}'.format(i)]

                if not title:
                    errors.append('title{}'.format(i))
                    msg = "Prosim vpišite naslov vseh fotografij!"
                    if msg not in msgs:
                        msgs.append(msg)

                file_ = File()
                file_.file = photo
                file_.user = request.user

                if (file_.file.size > settings.MAX_UPLOAD_SIZE or
                        file_.longer_edge() > settings.MAX_IMAGE_RESOLUTION):
                    errors.append('photo{}'.format(i))
                    msg = "Datoteka je prevelika!"
                    if msg not in msgs:
                        msgs.append(msg)

                files.append([file_, title])

        if len(files) == 0:
            msgs.append('Naložite vsaj eno fotografijo!')
            errors.append('photo1')

        if 'salonSelection' in request.POST:
            salon = Salon.objects.get(pk=request.POST['salonSelection'])
        else:
            msgs.append('Prosim izberite salon!')
            errors.append('salonSelection')

        if len(errors) == 0:
            theme = Theme.objects.filter(salon=salon)[0]

            for file_, title in files:
                file_.save()
                Photo.objects.create(title=title, user=request.user, theme=theme,
                                     photo=file_)

            logout(request)
            return redirect('upload_confirm')

    today = datetime.date.today()
    salons = Salon.objects.filter(start_date__lte=today, end_date__gte=today)

    response = {'salons': salons, 'msg': '<br>'.join(msgs)}
    for key in ['title1', 'title2', 'title3', 'salonSelection']:
        response[key] = request.POST[key] if key in request.POST else ''

    return render(request, os.path.join('uploader', 'upload.html'), response)


def list_select(request):
    salons = Salon.objects.all()

    response = {'salons': salons}
    return render(request, os.path.join('uploader', 'list_select.html'), response)


def list_details(request, salon_id):
    salon = get_object_or_404(Salon, pk=salon_id)
    themes = Theme.objects.filter(salon=salon)

    response = {'users': []}
    for user in UserProfile.objects.all():  # pylint: disable=no-member
        count = Photo.objects.filter(theme__in=themes, user=user).count()
        if count > 0:
            response['users'].append({
                'name': user.get_short_name,
                'school': user.school,
                'count': count})

    response['salon'] = salon
    return render(request, os.path.join('uploader', 'list_details.html'), response)


@csrf_exempt
def upload(request):
    if request.method != 'POST':
        logger.warning("Upload request other than POST.")
        return HttpResponseNotAllowed(['POST'], 'Only POST accepted')

    if not request.user.is_authenticated():
        logger.warning('Anonymous user tried to upload file.')
        return HttpResponseForbidden('Please login!')

    if request.FILES is None:
        logger.warning("Upload request without attached image.")
        return HttpResponseBadRequest('Must have files attached!')

    fn = request.FILES[u'files[]']
    logger.info("Image received.")

    file_ = File(file=fn, user=request.user)

    if file_.file.size > settings.MAX_UPLOAD_SIZE:
        logger.warning("Too big file.")
        return HttpResponseBadRequest("File can't excede size of {}KB".format(
            settings.MAX_UPLOAD_SIZE / 1024))

    if max(file_.file.width, file_.file.height) > settings.MAX_IMAGE_RESOLUTION:
        logger.warning("Too big file.")
        return HttpResponseBadRequest("File can't excede size of {}px".format(
            settings.MAX_IMAGE_RESOLUTION))

    file_.save()

    result = []
    result.append({"name": os.path.basename(file_.file.name),
                   "size": file_.file.size,
                   "url": file_.file.url,
                   "thumbnail": file_.thumbnail.url,  # pylint: disable=no-member
                   "delete_url": '',
                   "delete_type": "POST"})
    response_data = json.dumps(result)
    return HttpResponse(response_data, content_type='application/json')
