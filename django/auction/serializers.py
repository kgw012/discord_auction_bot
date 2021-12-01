from django.db.models.fields import IntegerField
from rest_framework import serializers

from .models import Player, Item


class PlayerNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['name']


class ItemListSerializer(serializers.ModelSerializer):
    bidders = PlayerNameSerializer(read_only=True, many=True)

    class Meta:
        model = Item
        fields = ['id', 'seq_id', 'name', 'bidders']


class AuctionListSerializer(serializers.ModelSerializer):
    reg_items = ItemListSerializer(read_only=True, many=True)
    class Meta:
        model = Player
        fields = ['id', 'name', 'reg_items']