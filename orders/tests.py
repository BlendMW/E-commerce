from django.test import TestCase
from django.contrib.auth.models import User
from .models import Order, OrderItem, Product
from decimal import Decimal
from django.urls import reverse

class OrderTestCase(TestCase):
    def setUp(self):
        # Setup test data
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Product.objects.create(name='Test Product', price=Decimal('50.00'))
        login_successful = self.client.login(username='testuser', password='12345')
        print(f"Login successful: {login_successful}")
        assert login_successful  # This will fail the setup if login was not successful.


    def test_order_creation(self):
        # Test order creation
        order = Order.objects.create(user=self.user)
        self.assertIsInstance(order, Order)

    def test_order_update(self):
        # Assuming you have a price field in OrderItem that needs to be explicitly set
        order = Order.objects.create(user=self.user)
        product_price = self.product.price
        OrderItem.objects.create(order=order, product=self.product, quantity=2, price=product_price)
        expected_total = product_price * 2
        self.assertEqual(order.calculate_total(), expected_total)

    def test_order_detail_view(self):
        # Create an order to test with
        order = Order.objects.create(user=self.user)
        url = reverse('order_details', kwargs={'order_id': order.id})  # Use 'order_id' to match your URLs
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_order_list_view(self):
        url = reverse('order_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_order_deletion(self):
        # Test order deletion
        order = Order.objects.create(user=self.user)
        order_id = order.id
        order.delete()
        with self.assertRaises(Order.DoesNotExist):
            Order.objects.get(id=order_id)
