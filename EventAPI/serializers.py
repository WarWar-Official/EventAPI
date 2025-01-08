from rest_framework import serializers
from django.utils.timezone import now
from .models import Event
from django.contrib.auth.models import User


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title','description','location','start_at']

    def validate(self, data):
        if len(data['description']) < 50:
            raise serializers.ValidationError('Description is too short.')
        if len(data['location']) < 5:
            raise serializers.ValidationError('Location is too short.')
        if data['start_at'] < now():
            raise serializers.ValidationError('Event cant be in the past.')
        return data
    
class EventEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id','title','description','location','start_at']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password','first_name','last_name']
    
    def validate(self, data):
        if (len(data['password'])<8):
            raise serializers.ValidationError("Password is too short.")
        return data

    def create(self, data):
        try:
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name'],
            )
        except KeyError as e:
            raise serializers.ValidationError("All fields are required.")
        return user
