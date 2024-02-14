from pyexpat import features
from django.db import models

class Product(models.Model):
    COLOR_CHOICES = (
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('black', 'Black'),
        ('white', 'White'),
        ('gray', 'Gray'),
        ('brown', 'Brown'),
        ('purple', 'Purple'),
        ('orange', 'Orange'),
        ('pink', 'Pink'),
    )
    SIZE_CHOICES = (
        ('xs', 'Extra Small'),
        ('s', 'Small'),
        ('m', 'Medium'),
        ('l', 'Large'),
        ('xl', 'Extra Large'),
        ('xxl', 'Double Extra Large'),
        ('xxxl', 'Triple Extra Large'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')
    available_colors = models.CharField(max_length=255, choices=COLOR_CHOICES, blank=True)
    available_sizes = models.CharField(max_length=255, choices=SIZE_CHOICES, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    features = models.TextField(blank=True)

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

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    color = models.CharField(max_length=255, choices=Product.COLOR_CHOICES)
    size = models.CharField(max_length=255, choices=Product.SIZE_CHOICES)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.color} - {self.size}"
