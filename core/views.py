from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


@swagger_auto_schema(
    methods=['post'],
    manual_parameters=[
        openapi.Parameter('username', openapi.IN_QUERY, description="username", type=openapi.TYPE_STRING),
        openapi.Parameter('email', openapi.IN_QUERY, description="email", type=openapi.TYPE_STRING),
        openapi.Parameter('password', openapi.IN_QUERY, description="password", type=openapi.TYPE_STRING),
    ],
    responses={201: BlogUserSerializer()},
)
@api_view(['POST'])
def create_user(request):
    serializer = BlogUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@swagger_auto_schema(
    methods=['put'],
    manual_parameters=[
        openapi.Parameter('username', openapi.IN_QUERY, description="username", type=openapi.TYPE_STRING),
        openapi.Parameter('email', openapi.IN_QUERY, description="email", type=openapi.TYPE_STRING),
        openapi.Parameter('password', openapi.IN_QUERY, description="password", type=openapi.TYPE_STRING),
        openapi.Parameter('bio', openapi.IN_QUERY, description="password", type=openapi.TYPE_STRING),
        openapi.Parameter('profile_picture', openapi.IN_QUERY, type=openapi.TYPE_FILE),
        openapi.Parameter('date_of_birth', openapi.IN_QUERY, type=openapi.TYPE_STRING),
    ],
    responses={202: BlogUserSerializer()},
    security=[{'Bearer': []}],
)
@swagger_auto_schema(
    method='DELETE',
    responses={204: "User account deleted successfully."},
    security=[{'Bearer': []}],
)
@api_view(['DELETE', 'PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_detail(request):
    user = request.user
    if request.method == 'PUT':
        data = request.data
        serializer = BlogUserSerializer(user, data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=202)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        user.delete()
        return JsonResponse({"message": "User account deleted successfully."}, status=204)


@swagger_auto_schema(
    method='GET',
    responses={200: PostSerializer(many=True)},
    security=[{'Bearer': []}],
)
@swagger_auto_schema(
    method='post',
    manual_parameters=[
        openapi.Parameter('title', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter('content', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter('image', openapi.IN_QUERY, type=openapi.TYPE_FILE),
        openapi.Parameter('categories', openapi.IN_QUERY, type=openapi.TYPE_ARRAY,
                          items=openapi.Items(type=openapi.TYPE_INTEGER)),
    ],
    responses={201: PostSerializer()},
)
@api_view(['GET', 'POST'])
@csrf_exempt
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = request.data
        print(data)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@swagger_auto_schema(
    method='GET',
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    ],
    responses={200: PostSerializer()},
    security=[{'Bearer': []}],
)
@swagger_auto_schema(
    method='put',
    manual_parameters=[
        openapi.Parameter('title', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter('content', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter('image', openapi.IN_QUERY, type=openapi.TYPE_FILE),
        openapi.Parameter('categories', openapi.IN_QUERY, type=openapi.TYPE_ARRAY,
                          items=openapi.Items(type=openapi.TYPE_INTEGER)),
    ],
    responses={201: PostSerializer()},
)
@swagger_auto_schema(
    method='DELETE',
    responses={204: "post deleted successfully"},
    security=[{'Bearer': []}],
)
@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        if request.user != post.author:
            return JsonResponse({"message": 'You is not the post author'}, status=403)
        data = request.data
        serializer = PostSerializer(post, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        if request.user != post.author:
            return JsonResponse({"message": 'You is not the post author'}, status=403)
        post.delete()
        return JsonResponse({"message": 'post deleted successfully'}, status=204)


@swagger_auto_schema(
    method='GET',
    responses={200: CategorySerializer(many=True)},
    security=[{'Bearer': []}],
)
@swagger_auto_schema(
    method='post',
    manual_parameters=[
        openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING),
    ],
    responses={201: CategorySerializer()},
)
@api_view(['GET', 'POST'])
@csrf_exempt
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = request.data
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@swagger_auto_schema(
    method='GET',
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    ],
    responses={200: CategorySerializer()},
    security=[{'Bearer': []}],
)
@swagger_auto_schema(
    method='put',
    manual_parameters=[
        openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING),
    ],
    responses={201: CategorySerializer()},
)
@swagger_auto_schema(
    method='DELETE',
    responses={204: "Category deleted successfully"},
    security=[{'Bearer': []}],
)
@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = request.data
        serializer = CategorySerializer(category, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        category.delete()
        return JsonResponse({"message": 'Delete successfully'}, status=204)


@api_view(['GET'])
@csrf_exempt
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def search_post(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10

    title = request.query_params.get('title', None)
    content = request.query_params.get('content', None)
    author_id = request.query_params.get('author', None)
    category_id = request.query_params.get('category', None)

    query = Q()
    if title:
        query |= Q(title__icontains=title)
    if content:
        query |= Q(content__icontains=content)
    if author_id:
        query &= Q(author_id=author_id)
    if category_id:
        query &= Q(categories__id=category_id)

    posts = Post.objects.filter(query).distinct()

    paginated_posts = paginator.paginate_queryset(posts, request)
    serializer = PostSerializer(paginated_posts, many=True)
    return paginator.get_paginated_response(serializer.data)
