from django.contrib import admin

from .models import File

class FileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['title']}),
        ('Date information', {'fields':['upl_date']}),
        (None, {'fields':['file']}),
        ]
    list_display = ('title', 'file', 'size', 'ctime', 'mtime', 'upl_date', 'was_uploaded_recently')

admin.site.register(File, FileAdmin)
