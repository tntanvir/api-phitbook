from django.shortcuts import render
from rest_framework import serializers,viewsets
# Create your views here.

from .models import Category
from .serializers import AllCategory

class categoryList(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = AllCategory
    def get_queryset(self):
        queryset = super().get_queryset()
        name=self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name=name)
        return queryset