import os

from django.shortcuts import render

from login.decorators import judge_required


@judge_required
def jury_app(request):
    return render(request, os.path.join('jury', 'app.html'))
