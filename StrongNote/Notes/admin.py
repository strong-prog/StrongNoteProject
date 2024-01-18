from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Notes, Category, Comment


class NotesAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Notes
        fields = '__all__'


class NotesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'created_at', 'get_photo', 'is_published', 'category')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_filter = ('is_published', 'id')
    list_editable = ['is_published', 'category']
    fields = ('title', 'content', 'photo', 'get_photo', 'is_published', 'created_at', 'updated_at', 'category')
    readonly_fields = ('get_photo', 'created_at', 'updated_at')
    form = NotesAdminForm

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')
        else:
            return 'Фото нет'

    get_photo.short_description = 'Миниатюра'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('note_connected', 'username', 'text', 'created')
    list_filter = ('created',)
    search_fields = ('username', 'text')


admin.site.register(Notes, NotesAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)

admin.site.site_title = 'Страница администратора'
admin.site.site_header = 'Страница администратора'
