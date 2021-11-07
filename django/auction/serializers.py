from rest_framework import serializers
from .models import Player, Item

class PlayerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name')


class ItemListSerializer(serializers.ModelSerializer):
    bidders = PlayerListSerializer(read_only=True, many=True)
    class Meta:
        model = Item
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    reg_items = ItemListSerializer(read_only=True, many=True)
    class Meta:
        model = Player
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    reg_player = PlayerListSerializer(read_only=True)
    bidders = PlayerListSerializer(read_only=True, many=True)
    class Meta:
        model = Item
        fields = '__all__'

