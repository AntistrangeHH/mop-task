from django.core import paginator
from django.core.paginator import Page
from rest_framework import pagination
from .serializers import RssItemSerializers

from .models import RssItem

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination


class RssItemsView(APIView):

    # Getting all the entries from the database
    def get(self, request):
        rss_item = RssItem.objects.all()
        # Paginate the pages by 10 entries
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(rss_item, request)
        # Serialize the paginated page
        serializer = RssItemSerializers(result_page, many=True)
        return Response(serializer.data)

    # If we want to force a post
    def post(self, request):
        serializer = RssItemSerializers(data=request)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)