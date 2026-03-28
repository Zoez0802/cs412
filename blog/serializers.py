# blog/serializers.py
# Serializers convert our django data models to a 
# text-representation suitable to transmit over HTTP.
 
from rest_framework import serializers
from .models import *
 
class ArticleSerializer(serializers.ModelSerializer):
  '''
  A serializer for the Article model.
  Specify which model/fields to send in the API.
  '''
 
  class Meta:
    model = Article
    fields = ['id', 'title', 'author', 'text', 'published', 'image_file']
   
  # add methods to customize the Create/Read/Update/Delete operations
    def create(self, validated_data):
        validated_data['user'] = User.objects.first()
        return Article.objects.create(**validated_data)