from __future__ import absolute_import, division, print_function, unicode_literals

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test, login_required


check_judge = user_passes_test(  # pylint: disable=invalid-name
    lambda usr: usr.is_judge(),
    login_url=settings.LOGIN_URL)


def judge_required(view_func):
    decorated_view_func = login_required(check_judge(view_func))
    return decorated_view_func
