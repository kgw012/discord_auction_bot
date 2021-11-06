from django.db import models
from django.db.models.deletion import CASCADE

class Player(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    reg_player = models.ForeignKey(Player, on_delete=CASCADE)
    bidders = models.ManyToManyField(Player, related_name='bid_items')

    def __str__(self):
        return f'{self.name}(등록자 \'{self.reg_player}\', self.created_at)'
