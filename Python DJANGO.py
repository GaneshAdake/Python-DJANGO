#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# models.py
from django.db import models

class Todo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

# serializers.py
from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'

# views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Todo
from .serializers import TodoSerializer

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    @action(detail=False, methods=['get'])
    def searchByTitle(self, request):
        title_query = request.query_params.get('title', '')
        todos = Todo.objects.filter(title__icontains=title_query)
        serializer = self.get_serializer(todos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def searchByDate(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
            todos = Todo.objects.filter(scheduled_at__range=(start_date, end_date))
            serializer = self.get_serializer(todos, many=True)
            return Response(serializer.data)
        else:
            return Response("Please provide start_date and end_date parameters.")

# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TodoViewSet

router = DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todo')

urlpatterns = [
    path('', include(router.urls)),
]

# settings.py (Add DRF to installed apps)
INSTALLED_APPS = [
    ...
    'rest_framework',
    ...
]


# In[ ]:




