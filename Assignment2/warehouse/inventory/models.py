from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

class Item(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=10)
    description = models.TextField(blank=True, null=True)
    stock = models.IntegerField(default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Purchase(BaseModel):
    code = models.CharField(max_length=100, unique=True)
    date = models.DateField()
    description = models.TextField()

class PurchaseDetail(models.Model):
    item_code = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    header_code = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='details')

class Sell(BaseModel):
    code = models.CharField(max_length=100, unique=True)
    date = models.DateField()
    description = models.TextField()

class SellDetail(models.Model):
    item_code = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    header_code = models.ForeignKey(Sell, on_delete=models.CASCADE, related_name='details')