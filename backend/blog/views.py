from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from blog.models import BlogPost
from blog.serializers import BlogPostSerializer
from django.utils.decorators import method_decorator


class BlogPostListView(ListAPIView):
    print("Comes in List View")
    queryset = BlogPost.objects.order_by('-date_created')
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
    permission_classes = (permissions.AllowAny, )


class BlogPostDetailView(RetrieveAPIView):
    queryset = BlogPost.objects.order_by('-date_created')
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
    permission_classes = (permissions.AllowAny, )


class BlogPostFeaturedView(ListAPIView):
    print("comes in featured")
    queryset = BlogPost.objects.all().filter(featured=True)
    print("queryset", queryset)
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
    permission_classes = (permissions.AllowAny, )


class BlogPostCategoryView(APIView):
    serializerclass = BlogPostSerializer
    permission_classes = (permissions.AllowAny, )

    
    def post(self, request, format=None):
        data = self.request.data
        category = data['category']
        queryset = BlogPost.objects.all().filter(category__iexact=category)
        
        serializer = BlogPostSerializer(queryset, many=True)

        return Response(serializer.data)