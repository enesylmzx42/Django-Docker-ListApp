from django.http import HttpResponse
from django.shortcuts import render
from .models import Todo
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import serializers



def todos(request):
    todos = Todo.objects.all()
    return render(request, 'todo/todos.html', {'todos': todos})

def edit_todo(request, pk):
    todo = Todo.objects.get(pk=pk)

    if request.method == 'POST':
        todo.title = request.POST.get('title', '')
        todo.save()
        return render(request, 'todo/partials/todo.html', {'todo': todo})
    
    return render(request, 'todo/partials/edit.html', {'todo': todo})

def add_todo(request):
    title = request.POST.get('title', '')

    if title: 
        todo = Todo.objects.create(title=title)
        return render(request, 'todo/partials/todo.html', {'todo': todo})
    else:
        return HttpResponse(status=400)
    
def undo_todo(request, pk):
    todo = Todo.objects.get(pk=pk)
    todo.is_done = False  
    todo.save()
    return render(request, 'todo/partials/todo.html', {'todo': todo})

def update_todo(request, pk):
    todo = Todo.objects.get(pk=pk)
    todo.is_done = True
    todo.save()
    return render(request, 'todo/partials/todo.html', {'todo': todo})

def delete_todo(request, pk):
    todo = Todo.objects.get(pk=pk)
    todo.delete()
    return HttpResponse()






@api_view(['GET', 'POST'])
def todo_list(request):
    if request.method == 'GET':
        todos = Todo.objects.all()
        serializer = serializers.TodoSerializer(todos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = serializers.TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
def todo_detail(request, pk):
    try:
        todo = Todo.objects.get(pk=pk)
    except Todo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.TodoSerializer(todo)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = serializers.TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
