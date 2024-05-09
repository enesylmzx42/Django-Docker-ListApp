from django.urls import path
from django.contrib import admin
from myapp.views import todos, add_todo, undo_todo, update_todo, delete_todo, edit_todo, todo_list, todo_detail

urlpatterns = [
    path('', todos, name='todos'),
    path('add-todo/', add_todo, name='add_todo'),
    path('update/<int:pk>/', update_todo, name='update_todo'),
    path('delete/<int:pk>/', delete_todo, name='delete_todo'),
    path('edit/<int:pk>/', edit_todo, name='edit_todo'),
    path('undo/<int:pk>/', undo_todo, name='undo_todo'),
    path('api/tasks/', todo_list, name='todo-list'),   
    path('api/tasks/<int:pk>/', todo_detail, name='todo-detail'),  
    path('admin/', admin.site.urls),
]

