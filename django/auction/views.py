from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Player, Item
from .serializers import PlayerListSerializer, PlayerSerializer, ItemListSerializer, ItemSerializer


@api_view(['GET', 'POST'])
def player_list_create(request):
    def player_list():
        players = Player.objects.all()
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)

    def player_create():
        serializer = PlayerListSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    if request.method == 'GET':
        return player_list()
    elif request.method == 'POST':
        return player_create()


@api_view(['GET', 'DELETE'])
def player_get_delete(request, player_pk):
    player = get_object_or_404(Player, pk=player_pk)

    def player_get():
        serializer = PlayerSerializer(player)
        return Response(serializer.data)

    def player_delete():
        player.delete()
        return Response(data='삭제 완료', status=status.HTTP_204_NO_CONTENT)
    
    if request.method == 'GET':
        return player_get()
    elif request.method == 'DELETE':
        return player_delete()


@api_view(['POST'])
def item_create(request, player_pk):
    reg_player = get_object_or_404(Player, pk=player_pk)
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(reg_player=reg_player)
        return Response(serializer.data)


@api_view(['GET'])
def item_list(request):
    items = Item.objects.all()
    serializer = ItemListSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['GET', 'DELETE'])
def item_get_delete(request, player_pk, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    def item_get():
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def item_delete():
        player = get_object_or_404(Player, pk=player_pk)
        
        # check player == item_reg_player
        if item.reg_player.pk != player.pk:
            return Response(data='아이템의 등록자만 삭제할 수 있습니다.', status=status.HTTP_403_FORBIDDEN)

        item.delete()
        return Response(data='삭제 완료', status=status.HTTP_204_NO_CONTENT)

    if request.method == 'GET':
        return item_get()
    elif request.method == 'DELETE':
        return item_delete()


@api_view(['POST'])
def bid(request, player_pk, item_pk):
    player = get_object_or_404(Player, pk=player_pk)
    item = get_object_or_404(Item, pk=item_pk)

    if item.bidders.filter(pk=player_pk).exists():
        item.bidders.remove(player)
        return Response(data='삭제 완료', status=status.HTTP_204_NO_CONTENT)
    else:
        item.bidders.add(player)
        return Response(data='저장 완료', status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def clear(request):
    Player.objects.all().delete()
    Item.objects.all().delete()
    return Response(data='모든 데이터 삭제 완료', status=status.HTTP_204_NO_CONTENT)
