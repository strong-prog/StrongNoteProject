from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User


class Notes(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    content = models.TextField(blank=True, verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    photo = models.ImageField(upload_to='media', verbose_name='Фото')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name='Категория')

    def get_absolute_url(self):
        return reverse_lazy('View_notes', kwargs={'pk': self.pk})

    @property
    def number_of_comments(self):
        return Comment.objects.filter(note_connected=self).count()

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['-created_at']


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Категория')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('Category', kwargs={'category_id': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Comment(models.Model):
    note_connected = models.ForeignKey(Notes, related_name='comments', on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    text = models.TextField(verbose_name='Текст комментария', max_length=3000)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created',)

    # def __str__(self):
    #     return str(self.username) + ', ' + self.note_connected.title[:40]
