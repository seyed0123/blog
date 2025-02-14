from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import *


class BlogUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Bolg_User
        fields = [
            'username', 'email', 'bio', 'profile_picture', 'date_of_birth', 'password'
        ]
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
        }

    def create(self, validated_data):
        user = Bolg_User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']  # you can use all that if you change the model does not need to change the serializer


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'content',
            'author',
            'image',
            'categories',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

        extra_kwargs = {
            'title': {'required': True},
            'content': {'required': True},
        }

    def create(self, validated_data):
        categories = validated_data.pop('categories', [])
        categories = map(int, categories)
        post = Post.objects.create(**validated_data)
        post.categories.set(categories)
        return post

    def update(self, instance, validated_data):
        categories = validated_data.pop('categories', None)
        if categories is not None:
            instance.categories.set(categories)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
