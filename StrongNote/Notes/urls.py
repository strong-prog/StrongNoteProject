from django.urls import path
# from django.views.decorators.cache import cache_page

from Notes.views import HomeNotes, NotesByCategory, ViewNotes,  register, user_login, user_logout

urlpatterns = [

    path('', HomeNotes.as_view(), name='Home'),
    path('category/<int:category_id>', NotesByCategory.as_view(), name='Category'),
    path('notes/<int:pk>', ViewNotes.as_view(), name='View_notes'),
    path('register/', register, name='Register'),
    path('login/', user_login, name='Login'),
    path('logout/', user_logout, name='Logout'),
]
