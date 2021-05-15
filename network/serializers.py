from django.db import models
from rest_framework import fields
from rest_framework.serializers import ModelSerializer
from .models import User, Advisor, Booking, BookingView

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class AdvisorSerializer(ModelSerializer):
    class Meta:
        model = Advisor
        fields = '__all__'

class BookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class BookingViewSerializer(ModelSerializer):
    class Meta:
        model = BookingView
        fields = '__all__'
