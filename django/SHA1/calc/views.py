import os

from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils import timezone

from .models import File
from .forms import ModelFormWithFileField

class IndexView(generic.ListView):
    template_name = 'calc/index.html'
    context_object_name = 'latest_file_list'

    def get_queryset(self):
        """
        Return the last five uploaded files (not including those set to be
        published in the future).
        """
        return File.objects.filter(upl_date__lte=timezone.now()).order_by('-upl_date')[:5]

class DetailView(generic.DetailView):
    model = File
    template_name = 'calc/detail.html'
    def get_queryset(self):
        """
        Excludes any files that aren't published yet.
        """
        return File.objects.filter(upl_date__lte=timezone.now())

def upload_file(request):
    if request.method == 'POST':
        form = ModelFormWithFileField(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/success/url/')
    else:
        form = ModelFormWithFileField(initial={'upl_date': timezone.now()})
    return render(request, 'calc/upload.html', {'form':form})
