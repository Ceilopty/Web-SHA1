import datetime, os
from django.db import models
from django.utils import timezone, module_loading

class File(models.Model):
    settings = module_loading.import_module(os.environ['DJANGO_SETTINGS_MODULE'])
    base = settings.MEDIA_ROOT
    upl_date = models.DateTimeField('date uploaded')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='files/%Y/%m/%d')
    sha = models.CharField('SHA1',max_length=64,default="")
    size = models.IntegerField('Size in Byte(s)',default=0)
    def abspath(self):
        return os.path.join(File.base,self.file.url)
    def __str__(self):
        return self.title
    def ctime(self):
        time = os.path.getctime(self.abspath())
        return datetime.datetime.fromtimestamp(time,timezone.get_current_timezone())
    ctime.short_description = 'Date Created'
    def mtime(self):
        time = os.path.getmtime(self.abspath())
        return datetime.datetime.fromtimestamp(time,timezone.get_current_timezone())
    mtime.short_description = 'Date Modified'
    def was_uploaded_recently(self):
        now = timezone.now()
        return now >= self.upl_date >= now - datetime.timedelta(days=1)
    was_uploaded_recently.admin_order_field = 'upl_date'
    was_uploaded_recently.boolean = True
    was_uploaded_recently.short_description = 'Uploaded recently?'
    def show(self):
        return zip(('title', 'file', 'size', 'upload date',
                    'create time', 'modify time'),
                   (self.title, self.file, self.size, self.upl_date,
                    self.ctime(), self.mtime()))

