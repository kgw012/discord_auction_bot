from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=50)
    item_sequence = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class Item(models.Model):
    seq_id = models.IntegerField()
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    reg_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='reg_items')
    bidders = models.ManyToManyField(Player, related_name='bid_items', blank=True)

    def __str__(self) -> str:
        return f'{self.name} ({self.reg_player.name})'
