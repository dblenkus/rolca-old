import os
from datetime import datetime

from django.shortcuts import render_to_response, HttpResponseRedirect, render
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import validate_email
from django.template import RequestContext

from .models import Application, Workshop


# pylint: disable=too-many-locals,too-many-branches
def application(request):
    """Main view for Workshops application


    """
    msgs = []
    typ = 0
    fields = ['institution', 'name', 'email', 'institution_name',
              'n_of_applicants']
    required = ['name', 'institution_name', 'email']
    values = {key: '' for key in fields}
    values['institution'] = False
    old_n_of_applicants = ''

    workshops = Workshop.objects.filter(start_date__gt=datetime.now()) \
        .extra(order_by=['start_date'])
    selected = {w.pk: False for w in workshops}

    if request.method == 'POST':
        values = {key: request.POST[key] if key in request.POST
                       else '' for key in fields}
        values['institution'] = True if values['institution'] else False

        old_n_of_applicants = values['n_of_applicants']
        if values['institution']:
            required.append('n_of_applicants')
        else:
            values['n_of_applicants'] = 1

        for key in required:
            if not values[key]:
                msg = "Prosim izpolnite obvezna polja."
                if msg not in msgs:
                    msgs.append(msg)
                typ |= 2 ** fields.index(key)

        selected = {w.pk: True if str(w.pk) in request.POST else False
                    for w in workshops}
        if not any(selected.values()):
            msgs.append("Prosim izberite vsaj eno delavnico.")
            typ |= 2 ** 5

        for pk in selected:  # pylint: disable=invalid-name
            if selected[pk]:
                # pylint: disable=invalid-name
                ws = Workshop.objects.get(pk=pk)  # TODO: remove this query
                if ws.limit and ws.limit - ws.count() < int(values['n_of_applicants']):
                    msgs.append("Ni dovolj prostih mest.")
                    typ |= 2 ** 5

        try:
            validate_email(values['email'])
        except ValidationError:
            msgs.append("Vnesite veljaven email naslov.")
            typ |= 2 ** 2

        if not typ:
            for workshop in workshops:
                if selected[workshop.pk]:
                    Application.objects.create(workshop=workshop, **values)

            return HttpResponseRedirect(reverse('confirm'))

    values['n_of_applicants'] = old_n_of_applicants
    response = {'workshops': workshops, 'msg': '<br/>'.join(msgs), 'type': typ,
                'selected': selected}
    response.update({key: values[key] for key in fields})
    context = RequestContext(request, response)
    template = os.path.join('workshops', 'application.html')
    return render_to_response(template, context)


def confirm(request):
    return render(request, os.path.join('workshops', 'confirm.html'))
