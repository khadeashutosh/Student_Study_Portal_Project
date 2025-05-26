from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),

    path('notes/',views.notes,name='notes'),
    path('delete_notes/<int:pk>',views.delete_notes,name='delete_notes'),
    path('notes_detail/<int:pk>',views.Notes_Detail_View.as_view(),name='notes_detail'),

    path('homework', views.homework, name='homework'),
    path('update_homework/<int:pk>',views.update_homework, name='updated_homework' ),
    path('delete_homework/<int:pk>', views.delete_homework, name='deleted_homework'),

    path('youtube', views.youtube,name='youtube'),  

    path('todo',views.todo,name='todo'),
    path('update_todo/<int:pk>',views.update_todo,name='updated-todos' ),
    path('delete_todo/<int:pk>', views.delete_todo, name='deleted_todo'),

    path('book', views.book, name='book'),

    path('dictionary', views.dictionary, name='dictionary'),

    path('wiki', views.wiki, name='wiki'),

    path('conversion', views.conversion, name='conversion')

]
