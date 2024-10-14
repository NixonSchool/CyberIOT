from django.contrib import admin
from .models import ContactFormSubmission
from .models import DataDownload

@admin.register(ContactFormSubmission)
class ContactFormSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at')
    list_filter = ('subject', 'submitted_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('submitted_at',)
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'phone', 'subject', 'message')
        }),
        ('Submission Info', {
            'fields': ('submitted_at',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        return False  # Prevents adding new submissions via admin

@admin.register(DataDownload)
class DataDownloadAdmin(admin.ModelAdmin):
    list_display = ('email', 'timestamp')

# from django.contrib import admin
# from .models import ContactFormSubmission
#
#
# @admin.register(ContactFormSubmission)
# class ContactFormSubmissionAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'subject', 'submitted_at')
#     list_filter = ('subject', 'submitted_at')
#     search_fields = ('name', 'email', 'subject', 'message')
#     readonly_fields = ('submitted_at',)
#
#     fieldsets = (
#         (None, {
#             'fields': ('name', 'email', 'phone', 'subject', 'message')
#         }),
#         ('Submission Info', {
#             'fields': ('submitted_at',),
#             'classes': ('collapse',)
#         }),
#     )
#
#     def has_add_permission(self, request):
#         return False  # Prevents adding new submissions via admin
#
#     def has_delete_permission(self, request, obj=None):
#         return False  # Optionally disable deletion
#
#     def has_change_permission(self, request, obj=None):
#         if obj is not None:
#             return True  # Allow editing existing submissions
#         return False  # Disallow creating new submissions
#
#     def get_readonly_fields(self, request, obj=None):
#         if obj is None:
#             # When adding a new submission, make all fields read-only
#             return [field.name for field in self.model._meta.fields]
#         return super().get_readonly_fields(request, obj)
