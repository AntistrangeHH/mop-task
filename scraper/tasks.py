from . import config
from .serializers import RssItemSerializers

import feedparser

from celery import Celery
from celery.schedules import crontab

from rest_framework.response import Response
from rest_framework import status


app = Celery('tasks')


@app.task
def ScrapeData():
    count = 0
    for symbol in config.nasdaq_symbols:

        url = config.url.format(symbol)
        news_feed = feedparser.parse(url)

        for entry in news_feed.entries:

            data = {}
            data["description"] = entry["summary"]
            data["guid"] = entry["id"]
            data["link"] = entry["link"]
            date = entry.published_parsed
            data["date"] = '{0}-{1}-{2}'.format(date.tm_year, date.tm_mon, date.tm_mday)
            data["title"] = entry["title"]
            data["symbol"] = symbol

            # Serializing the data
            serializer = RssItemSerializers(data=data)
            if serializer.is_valid():
                serializer.save()
                count+=1
            else:
                response = serializer.errors
                # This gets the number of entries that succeded in case of error
                response["finished"] = count
                # This is the entry that failed 
                response["entry_that_failed"] = data
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

    return Response("Saved "+str(count), status=status.HTTP_201_CREATED)