from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Player, Item
from .serializers import AuctionListSerializer


@api_view(['GET'])
def list_auction(request):
    players = Player.objects.all()
    serializer = AuctionListSerializer(instance=players, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
