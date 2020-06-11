from django.test import TestCase
from rest_framework.test import APIClient

from .views import StockPriceList
from .models import PCUser, Interest, Stock, StockPrice

class UserTestCase(TestCase):
    """
    Tests User objects
    """
    def setUp(self):
        Interest.objects.create(interest='int1')
        Interest.objects.create(interest='int2')
        Interest.objects.create(interest='int3')
        PCUser.objects.create(username="testcaseuser1", password="1234")

    def test_can_add_single_interest(self):
        # Arrange
        int1 = Interest.objects.get(pk='1')
        user1 = PCUser.objects.get(username='testcaseuser1')
        
        # Act
        user1.interests.add(int1)

        # Assert
        user1Ints = list(user1.interests.all())
        self.assertNotEquals(user1Ints, [])
        self.assertEquals(user1Ints, [int1])

    def test_can_add_many_interests(self):
        # Arrange
        ints = Interest.objects.all()
        user1 = PCUser.objects.get(username='testcaseuser1')

        # Act
        for int in ints:
            user1.interests.add(int)

        # Assert
        user1Ints = list(user1.interests.all())
        self.assertNotEquals(user1Ints, [])
        self.assertEquals(user1Ints, list(ints))

    def test_can_remove_interests(self):
        # Arrange
        ints = Interest.objects.all()
        user1 = PCUser.objects.get(username='testcaseuser1')

        # Act
        for int in ints:
            user1.interests.add(int)

        user1.interests.remove(Interest.objects.get(pk='1'))

        # Assert
        user1Ints = list(user1.interests.all())
        self.assertNotEquals(user1Ints, [])
        self.assertEquals(user1Ints, list(Interest.objects.filter(pk__gt='1')))

class StockPriceTestCase(TestCase):
    """
    Tests stock price objects
    """
    def setUp(self):
        stock1 = Stock.objects.create(name='test1', symbol='tst1', category='testCat')
        StockPrice.objects.create(stock=stock1, date='2020-01-01', opening_price='5.00')
        StockPrice.objects.create(stock=stock1, date='2020-01-02', opening_price='5.05')

    def test_can_create_stock_price(self):
        # Arrange
        client = APIClient()

        # Act
        response = client.post('/api/v1/stock-price/', {'stock': 1, 'date': '2020-01-01', 'opening_price': '5.00'})

        # Assert
        self.assertEquals(response.status_code, 201)

    def test_get_all_stock_prices(self):
        # Arrange
        client = APIClient()
        expectedData = [
            {'id': 1, 'stock': 1, 'date': '2020-01-01', 'opening_price': '5.00', 'predicted_closing_price': None},
            {'id': 2, 'stock': 1, 'date': '2020-01-02', 'opening_price': '5.05', 'predicted_closing_price': None},
            ]

        # Act
        response = client.get('/api/v1/stock-price/')

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, expectedData)

    def test_get_a_stock_price(self):
        # Arrange
        client = APIClient()
        expectedData = {'id': 2, 'stock': 1, 'date': '2020-01-02', 'opening_price': '5.05', 'predicted_closing_price': None}

        # Act 
        response = client.get('/api/v1/stock-price/2')

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, expectedData)

    def test_err_get_invalid_stock_price(self):
        # Arrange
        client = APIClient()

        # Act 
        response = client.get('/api/v1/stock-price/3')

        # Assert
        self.assertEquals(response.status_code, 404)

    def test_can_patch_stock_price(self):
        # Arrange
        client = APIClient()
        expectedData = {'id': 2, 'stock': 1, 'date': '2020-01-02', 'opening_price': '5.06', 'predicted_closing_price': None}

        # Act
        response = client.patch('/api/v1/stock-price/2', {'opening_price': '5.06'})

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, expectedData)
        
    def test_err_patch_invalid_id(self):
        # Arrange
        client = APIClient()
        updatedObject = {'stock': 1, 'date': '2020-01-02', 'opening_price': '5.07', 'predicted_closing_price': ''}

        # Act
        response = client.patch('/api/v1/stock-price/3', updatedObject)

        # Assert
        self.assertEquals(response.status_code, 404)
        
    def test_can_put_stock_price(self):
        # Arrange
        client = APIClient()
        updatedObject = {'stock': 1, 'date': '2020-01-02', 'opening_price': '5.07', 'predicted_closing_price': ''}
        expectedData = {'id': 2, 'stock': 1, 'date': '2020-01-02', 'opening_price': '5.07', 'predicted_closing_price': None}

        # Act
        response = client.put('/api/v1/stock-price/2', updatedObject)

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, expectedData) 
        
    def test_err_put_invalid_id(self):
        # Arrange
        client = APIClient()
        updatedObject = {'stock': 1, 'date': '2020-01-02', 'opening_price': '5.07', 'predicted_closing_price': ''}

        # Act
        response = client.put('/api/v1/stock-price/3', updatedObject)

        # Assert
        self.assertEquals(response.status_code, 404)
    
    def test_err_delete_stock_price(self):
        # Arrange
        client = APIClient()

        # Act 
        response = client.delete('/api/v1/stock-price/2')

        # Assert
        self.assertEquals(response.status_code, 405)

class StockTestCase(TestCase):
    """
    Tests stock objects
    """
    def setUp(self):
        stock1 = Stock.objects.create(name='test1', symbol='tst1', category='cat1')
        stock2 = Stock.objects.create(name='test2', symbol='tst2', category='cat2')

        StockPrice.objects.create(stock=stock1, date='2020-01-01', opening_price='5.00')
        StockPrice.objects.create(stock=stock1, date='2020-01-02', opening_price='5.05')
        StockPrice.objects.create(stock=stock1, date='2020-01-03', opening_price='5.10')

        StockPrice.objects.create(stock=stock2, date='2020-01-01', opening_price='6.00')
        StockPrice.objects.create(stock=stock2, date='2020-01-02', opening_price='6.05')
        StockPrice.objects.create(stock=stock2, date='2020-01-03', opening_price='6.10')

    def test_get_all_stocks(self):
        # Arrange
        client = APIClient()
        expectedData = [
            {'id': 1, 'name': 'test1', 'symbol': 'tst1', 'category': 'cat1', 'stock_prices': [1, 2, 3]},
            {'id': 2, 'name': 'test2', 'symbol': 'tst2', 'category': 'cat2', 'stock_prices': [4, 5, 6]},
            ]

        # Act
        response = client.get('/api/v1/stock/')
        
        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, expectedData)

    def test_get_a_stock(self):
        # Arrange
        client = APIClient()
        expectedData = {'id': 2, 'name': 'test2', 'symbol': 'tst2', 'category': 'cat2', 'stock_prices': [4, 5, 6]}

        # Act
        response = client.get('/api/v1/stock/2')
        
        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, expectedData)

    def test_err_get_invalid_stock(self):
        # Arrange
        client = APIClient()

        # Act 
        response = client.get('/api/v1/stock/3')

        # Assert
        self.assertEquals(response.status_code, 404)

    def test_err_create_stock(self):
        # Arrange
        client = APIClient()

        # Act 
        response = client.post('/api/v1/stock/', {'name': 'test3', 'symbol': 'tst3', 'category': 'cat3'})

        # Assert
        self.assertEquals(response.status_code, 405)
    
    def test_err_update_stock(self):
        # Arrange
        client = APIClient()

        # Act 
        response = client.put('/api/v1/stock/2', {'category': 'cat2'})

        # Assert
        self.assertEquals(response.status_code, 405)
    
    def test_err_delete_stock(self):
        # Arrange
        client = APIClient()

        # Act 
        response = client.delete('/api/v1/stock/2')

        # Assert
        self.assertEquals(response.status_code, 405)
