from django.test import TestCase
from .models import RssItem
from .serializers import RssItemSerializers
from rest_framework import status
from django.urls import reverse 
from django.urls import client
import json
# Create your tests here.



class GetAllFeed(TestCase):

     def test_get_all_puppies(self):
        # get API response
        response = client.get(reverse('/'))
        # get data from db
        puppies = RssItem.objects.all()
        serializer = RssItemSerializers(puppies, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PostRssFeed(TestCase):

       def setUp(self):
        self.valid_payload = {
            "description": "In this article, we discuss the 10 meme stocks that more than doubled in 2021. If you want to skip our detailed analysis of these stocks, go directly to the 5 Meme Stocks that More than Doubled in 2021. Meme stocks have exploded in popularity at the stock market. According to a study by investment […]",
            "guid": "ec775ee8-43e9-33a5-8d5b-5d62b367f3c7",
            "link": "https://finance.yahoo.com/news/10-meme-stocks-more-doubled-181816031.html?.tsrc=rss",
            "date": "2021-11-27",
            "title": "10 Meme Stocks that More than Doubled in 2021",
            "symbol": "AAPL"
        }
        self.invalid_payload = {
           "description": "In this article, we discuss the 10 meme stocks that more than doubled in 2021. If you want to skip our detailed analysis of these stocks, go directly to the 5 Meme Stocks that More than Doubled in 2021. Meme stocks have exploded in popularity at the stock market. According to a study by investment […]",
            "guid": "ec775ee8-43e9-33a5-8d5b-5d62b367f3c7",
            "link": "https://finance.yahoo.com/news/10-meme-stocks-more-doubled-181816031.html?.tsrc=rss",
            "date": "",
            "title": "10 Meme Stocks that More than Doubled in 2021",
            "symbol": "AAPL"
        }

        def test_create_valid_rss(self):
            response = client.post(
                reverse('/'),
                data=json.dumps(self.valid_payload),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        def test_create_invalid_rss(self):
            response = client.post(
                reverse('/'),
                data=json.dumps(self.invalid_payload),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)