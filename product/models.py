from pyexpat import features
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')
    colors = models.CharField(max_length=255, blank=True)  # Simple comma-separated colors
    size = models.CharField(max_length=255, blank=True)  # Simple comma-separated sizes
    quantity = models.PositiveIntegerField(default=0)
    features = models.TextField(blank=True)  # Simple comma-separated features
    # Rating could be an average dynamically calculated from reviews
    
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    
    def __str__(self):
        return f"{self.product.name} Image"

class ProductVideo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    video = models.FileField(upload_to='product_videos/')
    
    def __str__(self):
        return f"{self.product.name} Video"

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False, help_text='Indicates if the review has been approved by a moderator.')
    
    def __str__(self):
        return f"Review by {self.user.username} on {self.product.name}"
