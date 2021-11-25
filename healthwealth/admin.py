from django.contrib import admin
from .services import DocumentService
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from .models import DocumentAccess, User
from .models import Document


admin.site.site_header = "Health Wealth"
admin.site.site_title = "Health Wealth Portal"
admin.site.index_title = "Health Wealth Portal"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Define admin model for custom User model with no username field."""

    search_fields = ['email', 'full_name']
    readonly_fields = ("id",)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['file_download', 'id', 'title', 'uploaded_by', 'uploaded_at']
    list_display_links = ['id']
    search_fields = ['file_name', 'uploaded_by']
    readonly_fields = ['file_download', 'id']
    autocomplete_fields = ['uploaded_by']
    list_filter = ['category']

    def save_model(self, request):
        return DocumentService().save_file(request.user, request.FILES['content'], '')

    def file_download(self, instance):
        if instance.id:
            return format_html('<a href="{}" download="{}">Download</a>',
                               instance.document_url, instance.file_name)
        return '-'

    class Meta:
        ordering = ['-uploaded_at']


@admin.register(DocumentAccess)
class DocumentAccessAdmin(admin.ModelAdmin):
    list_display = ['user', 'document', 'access_granted_date']

    class Meta:
        ordering = ['-access_granted_date']
