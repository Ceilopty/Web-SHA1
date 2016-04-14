import os

from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from hashlib import sha1

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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context['file'].sha:
            path = context['file'].abspath()
            s = sha1()
            with open(path,'rb')as f:
                while 1:
                    chunk = f.read(4096)
                    s.update(chunk)
                    if not chunk:break
            context['file'].size = os.path.getsize(path)
            context['file'].sha = s.hexdigest()
            context['file'].save()
        return context

def upload_file(request):
    if request.method == 'POST':
        form = ModelFormWithFileField(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('calc:success'))
    else:
        form = ModelFormWithFileField(initial={'upl_date': timezone.now()})
    return render(request, 'calc/upload.html', {'form':form})

def upload_success(request):
    return render(request, 'calc/success.html')
