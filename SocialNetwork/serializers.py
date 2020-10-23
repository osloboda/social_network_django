from rest_framework import serializers
from .models import POST, LIKE


class POSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = POST
        fields = ['title', 'text']


class LIKESerializer(serializers.ModelSerializer):
    class Meta:
        model = LIKE
        fields = []