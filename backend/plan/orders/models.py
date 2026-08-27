from django.db import models

# Create your models here.
class Orders(models.Model):
   class OrderStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'
   status = models.CharField(max_length=10, choices=OrderStatus.choices, default=OrderStatus.PENDING)
   buyer=models.ForeignKey('users.Buyer', on_delete=models.CASCADE, blank=True, null=True)
   product=models.ForeignKey('catalogue.Catalogue', on_delete=models.CASCADE, related_name='product_orders')
   amount=models.ForeignKey('catalogue.Catalogue', on_delete=models.CASCADE, related_name='amount_orders', default=0)
   created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
   updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


def __str__(self):
        return f"Order {self.id}"

class payments(models.Model):
     class paymentsChoices(models.TextChoices):
        MPESA = 'MPESA', 'MPESA'
        CARD = 'CARD', 'Card'
     orders=models.ForeignKey(Orders, on_delete=models.CASCADE)
     payment_method=models.CharField(choices=paymentsChoices.choices, default=paymentsChoices.MPESA, max_length=10) 

def __str__(self):
        return f"Payment {self.id}"