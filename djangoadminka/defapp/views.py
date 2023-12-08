from django.conf import settings
from django.shortcuts import render


def index(request):
    context = {}
    if settings.DEBUG:
        context['text'] = {
            'txt': settings.CSRF_TRUSTED_ORIGINS,
            'DEBUG': settings.DEBUG,
        }
    return render(
        request,
        template_name='defapp/index.html',
        context=context
    )
