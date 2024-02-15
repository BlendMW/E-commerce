from django.db import models
from django.conf import settings
from product.models import Product

SHIPPING_STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Processing', 'Processing'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
]

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    shipping_status = models.CharField(max_length=50, default='Pending', choices=SHIPPING_STATUS_CHOICES)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    shipping_address = models.TextField(blank=True, null=True)
    products = models.ManyToManyField(Product, through='OrderItem')
    
    def add_item(self, product, quantity=1):
        order_item, created = self.items.get_or_create(
            product=product, 
            defaults={'price': product.price, 'quantity': quantity}
        )
        if not created:
            order_item.quantity += quantity
            order_item.save()

    def calculate_total(self):
        return sum(item.price * item.quantity for item in self.items.all())

    @classmethod
    def create_order(cls, user, products):
        order = cls.objects.create(user=user)
        for product, quantity in products.items():
            order.add_item(product, quantity)
        return order

    def update_order_status(self, new_status):
        self.shipping_status = new_status
        self.save()

    def apply_discount(self, discount_code):
        # Implement discount code application here
        pass

    def add_shipping_cost(self, shipping_cost):
        # Implement shipping cost addition here
        pass

    def handle_refund(self):
        # Implement refund logic here
        pass

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order.id})"
