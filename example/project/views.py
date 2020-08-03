from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseRedirect
try:
    from django.urls import reverse
except ModuleNotFoundError as e:
    # for Django < v1.10
    from django.core.urlresolvers import reverse
from upload_form import app_settings as upload_form_app_settings
from .forms import MyUploadForm
from .models import File


def index(request):

    assert request.method == 'GET'
    form = MyUploadForm()

    app_settings = [
        ['UPLOAD_FORM_MAX_FILE_SIZE_MB', upload_form_app_settings.get_max_file_size_MB()],
        ['UPLOAD_FORM_PARALLEL_UPLOAD', upload_form_app_settings.get_parallel_upload()],
        ['UPLOAD_FORM_ALLOWED_FILE_TYPES', ', '.join(upload_form_app_settings.get_allowed_file_types())],
    ]

    return render(
        request,
        'index.html', {
            'app_settings': app_settings,
            'form': form,
            'form_as_html': form.as_html(request),
            'files': File.objects.all()
        }
    )


def my_upload_target_view(request):

    assert request.method == 'POST'
    assert request.is_ajax()

    form = MyUploadForm(request.POST, request.FILES)
    if form.is_valid():
        url = form.form_valid(request)
        return JsonResponse({'action': 'redirect', 'url': url, })
    else:
        return JsonResponse({'action': 'replace', 'html': form.as_html(request), })


def clear_all_files(request):
    File.objects.all().delete()
    return HttpResponseRedirect(reverse('index'))
