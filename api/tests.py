from datetime import date

from django.test import TestCase
from django.contrib.auth.models import Permission
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from .models import PCUser, Interest, Stock, StockPrice
from .utils import stock_suggestions

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
        regularUser = PCUser.objects.create_user('regular', password='1234')
        specialUser = PCUser.objects.create_user('special', password='1234')
        specialUser.user_permissions.add(Permission.objects.get(codename='add_stockprice'))
        specialUser.user_permissions.add(Permission.objects.get(codename='change_stockprice'))
        specialUser.user_permissions.add(Permission.objects.get(codename='delete_stockprice'))
        specialUser.save()

        self.rUserToken = APIClient().post('/api/v1/rest-auth/login/', {'username': 'regular', 'password': '1234'}).data['key']
        self.sUserToken = APIClient().post('/api/v1/rest-auth/login/', {'username': 'special', 'password': '1234'}).data['key']

        stock1 = Stock.objects.create(name='test1', symbol='tst1', category='testCat')
        StockPrice.objects.create(stock=stock1, date='2020-01-01', opening_price='5.00')
        StockPrice.objects.create(stock=stock1, date='2020-01-02', opening_price='5.05')

    def test_create_stock_price(self):
        expectedData = {'id': 3, 'stock': 'tst1', 'date': '2020-01-01', 'opening_price': '5.00', 'predicted_closing_price': None}
        
        # Arrange (special user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.sUserToken)

        # Act
        response = client.post('/api/v1/stock-price/', {'stock': 'tst1', 'date': '2020-01-01', 'opening_price': '5.00'})

        # Assert
        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.data, expectedData)


        # Arrange (regular user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.rUserToken)

        # Act
        response = client.post('/api/v1/stock-price/', {'stock': 'tst1', 'date': '2020-01-01', 'opening_price': '5.00'})

        # Assert
        self.assertEquals(response.status_code, 403)

    def test_get_all_stock_prices(self):
        expectedData = [
            {'id': 1, 'stock': 'tst1', 'date': '2020-01-01', 'opening_price': '5.00', 'predicted_closing_price': None},
            {'id': 2, 'stock': 'tst1', 'date': '2020-01-02', 'opening_price': '5.05', 'predicted_closing_price': None},
            ]

        # Arrange (special user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.sUserToken)
    
        # Act
        response = client.get('/api/v1/stock-price/')
    
        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, expectedData)


        # Arrange (regular user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.rUserToken)
    
        # Act
        response = client.get('/api/v1/stock-price/')
    
        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, expectedData)
    
    def test_get_a_stock_price(self):
        expectedData = {'id': 2, 'stock': 'tst1', 'date': '2020-01-02', 'opening_price': '5.05', 'predicted_closing_price': None}

        # Arrange (special user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.sUserToken)
    
        # Act 
        response = client.get('/api/v1/stock-price/2')
    
        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, expectedData)


        # Arrange (regular user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.rUserToken)
    
        # Act 
        response = client.get('/api/v1/stock-price/2')
    
        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, expectedData)
    
    def test_err_get_invalid_stock_price(self):
        # Arrange
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.rUserToken)
    
        # Act 
        response = client.get('/api/v1/stock-price/3')
    
        # Assert
        self.assertEquals(response.status_code, 404)
    
    def test_can_patch_stock_price(self):
        expectedData = {'id': 2, 'stock': 'tst1', 'date': '2020-01-02', 'opening_price': '5.06', 'predicted_closing_price': None}

        # Arrange (special user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.sUserToken)
    
        # Act
        response = client.patch('/api/v1/stock-price/2', {'opening_price': '5.06'})
    
        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, expectedData)


        # Arrange (regular user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.rUserToken)
    
        # Act
        response = client.patch('/api/v1/stock-price/2', {'opening_price': '5.06'})
    
        # Assert
        self.assertEquals(response.status_code, 403)
        
    def test_err_patch_invalid_id(self):
        # Arrange
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.sUserToken)
        updatedObject = {'stock': 'tst1', 'date': '2020-01-02', 'opening_price': '5.07', 'predicted_closing_price': ''}
    
        # Act
        response = client.patch('/api/v1/stock-price/3', updatedObject)
    
        # Assert
        self.assertEquals(response.status_code, 404)
        
    def test_can_put_stock_price(self):
        expectedData = {'id': 2, 'stock': 'tst1', 'date': '2020-01-02', 'opening_price': '5.07', 'predicted_closing_price': None}
   
        # Arrange (special user)
        client = APIClient
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.sUserToken)
        updatedObject = {'stock': 'tst1', 'date': '2020-01-02', 'opening_price': '5.07', 'predicted_closing_price': ''}
    
        # Act
        response = client.put('/api/v1/stock-price/2', updatedObject)
    
        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, expectedData) 
   
   
        # Arrange (regular user)
        client = APIClient
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.rUserToken)
        updatedObject = {'stock': 'tst1', 'date': '2020-01-02', 'opening_price': '5.07', 'predicted_closing_price': ''}
    
        # Act
        response = client.put('/api/v1/stock-price/2', updatedObject)
    
        # Assert
        self.assertEquals(response.status_code, 403) 
        
    def test_err_put_invalid_id(self):
        # Arrange
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.sUserToken)
        updatedObject = {'stock': 'tst1', 'date': '2020-01-02', 'opening_price': '5.07', 'predicted_closing_price': ''}
    
        # Act
        response = client.put('/api/v1/stock-price/3', updatedObject)
    
        # Assert
        self.assertEquals(response.status_code, 404)
    
    def test_err_delete_stock_price(self):
        # Arrange
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.rUserToken)
    
        # Act 
        response = client.delete('/api/v1/stock-price/1')
    
        # Assert
        self.assertEquals(response.status_code, 403)

class StockTestCase(TestCase):
    """
    Tests stock objects
    """
    def setUp(self):
        regularUser = PCUser.objects.create_user('regular', password='1234')
        specialUser = PCUser.objects.create_user('special', password='1234')
        specialUser.user_permissions.add(Permission.objects.get(codename='add_stock'))
        specialUser.user_permissions.add(Permission.objects.get(codename='change_stock'))
        specialUser.user_permissions.add(Permission.objects.get(codename='delete_stock'))
        specialUser.save()

        self.rUserToken = APIClient().post('/api/v1/rest-auth/login/', {'username': 'regular', 'password': '1234'}).data['key']
        self.sUserToken = APIClient().post('/api/v1/rest-auth/login/', {'username': 'special', 'password': '1234'}).data['key']

        stock1 = Stock.objects.create(name='test1', symbol='tst1', category='cat1')
        stock2 = Stock.objects.create(name='test2', symbol='tst2', category='cat2')

        StockPrice.objects.create(stock=stock1, date='2020-01-01', opening_price='5.00')
        StockPrice.objects.create(stock=stock1, date='2020-01-02', opening_price='5.05')
        StockPrice.objects.create(stock=stock1, date='2020-01-03', opening_price='5.10')

        StockPrice.objects.create(stock=stock2, date='2020-01-01', opening_price='6.00')
        StockPrice.objects.create(stock=stock2, date='2020-01-02', opening_price='6.05')
        StockPrice.objects.create(stock=stock2, date='2020-01-03', opening_price='6.10')

    def test_get_all_stocks(self):
        expectedData = [
            {'name': 'test1', 'symbol': 'tst1', 'category': 'cat1', 'stock_prices': [1, 2, 3]},
            {'name': 'test2', 'symbol': 'tst2', 'category': 'cat2', 'stock_prices': [4, 5, 6]},
            ]

        # Arrange (special user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.sUserToken)

        # Act
        response = client.get('/api/v1/stock/')
        
        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, expectedData)
        

        # Arrange (regular user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.sUserToken)

        # Act
        response = client.get('/api/v1/stock/')
        
        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, expectedData)

    def test_get_a_stock(self):
        expectedData = {'name': 'test2', 'symbol': 'tst2', 'category': 'cat2', 'stock_prices': [4, 5, 6]}

        # Arrange (special user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.sUserToken)

        # Act
        response = client.get('/api/v1/stock/2')
        
        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, expectedData)


        # Arrange (regular user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.rUserToken)

        # Act
        response = client.get('/api/v1/stock/2')
        
        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, expectedData)

    def test_err_get_invalid_stock(self):
        # Arrange
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.rUserToken)

        # Act 
        response = client.get('/api/v1/stock/3')

        # Assert
        self.assertEquals(response.status_code, 404)

    def test_create_stock(self):
        expectedData = {'name': 'test3', 'symbol': 'tst3', 'category': 'cat3', 'stock_prices': []}

        # Arrange (special user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.sUserToken)

        # Act 
        response = client.post('/api/v1/stock/', {'name': 'test3', 'symbol': 'tst3', 'category': 'cat3'})

        # Assert
        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.data, expectedData)


        # Arrange (regular user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.rUserToken)

        # Act 
        response = client.post('/api/v1/stock/', {'name': 'test3', 'symbol': 'tst3', 'category': 'cat3'})

        # Assert
        self.assertEquals(response.status_code, 403)
    
    def test_patch_stock(self):
        expectedData = {'name': 'test2', 'symbol': 'tst2', 'category': 'cat3', 'stock_prices': [4, 5, 6]}

        # Arrange (special user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.sUserToken)

        # Act 
        response = client.patch('/api/v1/stock/2', {'category': 'cat3'})

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, expectedData)


        # Arrange (regular user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.rUserToken)

        # Act 
        response = client.patch('/api/v1/stock/2', {'category': 'cat3'})

        # Assert
        self.assertEquals(response.status_code, 403)
    
    def test_put_stock(self):
        expectedData = {'name': 'test2', 'symbol': 'tst2', 'category': 'cat3', 'stock_prices': [4, 5, 6]}

        # Arrange (special user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.sUserToken)

        # Act 
        response = client.put('/api/v1/stock/2', {'name': 'test2', 'symbol': 'tst2', 'category': 'cat3', 'stock_prices': [4, 5, 6]})

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, expectedData)
        

        # Arrange (regular user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.rUserToken)

        # Act 
        response = client.put('/api/v1/stock/2', {'name': 'test2', 'symbol': 'tst2', 'category': 'cat3', 'stock_prices': [4, 5, 6]})

        # Assert
        self.assertEquals(response.status_code, 403)
    
    def test_delete_stock(self):
        # Arrange (special user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.sUserToken)

        # Act 
        response = client.delete('/api/v1/stock/2')

        # Assert
        self.assertEquals(response.status_code, 204)

        
        # Arrange (regular user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.rUserToken)

        # Act 
        response = client.delete('/api/v1/stock/2')

        # Assert
        self.assertEquals(response.status_code, 403)

class SuggestionViewTestCase(TestCase):
    """
    Tests the suggestion view, does not test the suggestion algorithm
    """
    def setUp(self):
        user = PCUser.objects.create_user('regular', password='1234')

        self.userToken = APIClient().post('/api/v1/rest-auth/login/', {'username': 'regular', 'password': '1234'}).data['key']

        stock1 = Stock.objects.create(name='test1', symbol='tst1', category='testCat')
        StockPrice.objects.create(stock=stock1, date=date.today(), opening_price='5.00', predicted_closing_price="10.00")
        StockPrice.objects.create(stock=stock1, date=date.today(), opening_price='5.00', predicted_closing_price="0.00")

    def test_must_be_authenticated(self):
        # Arrange
        client = APIClient()

        # Act 
        response = client.get('/api/v1/suggestion/')

        # Assert
        self.assertEquals(response.status_code, 401)

    def test_can_get_suggestions(self):
        # Arrange
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.userToken)

        # Act 
        response = client.get('/api/v1/suggestion/')

        # Assert
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(dict(response.data)['suggestions']), 2)   # Test that it returned two predictions

class SuggestionAlgorithmTestCase(TestCase):
    """
    Tests the suggestion algorithm
    """
    def test_beyond_thresholds(self):
        # Arrange
        stock1 = Stock.objects.create(name='test1', symbol='tst1', category='testCat')
        StockPrice.objects.create(stock=stock1, date=date.today(), opening_price='1.00', predicted_closing_price="2.00")    #  1.0 change
        StockPrice.objects.create(stock=stock1, date=date.today(), opening_price='1.00', predicted_closing_price="0.00")    # -1.0 change
        prices = StockPrice.objects.filter(stock=stock1)

        expected = [{'stock': 'tst1', 'action': 'buy', 'percent_change': 1.0}, {'stock': 'tst1', 'action': 'sell', 'percent_change': -1.0}, ]

        # Act
        result = stock_suggestions(prices, -0.1, 0.1)

        # Assert
        self.assertEqual(result, expected)
        
    def test_at_thresholds(self):
        # Arrange
        stock1 = Stock.objects.create(name='test1', symbol='tst1', category='testCat')
        StockPrice.objects.create(stock=stock1, date='2020-01-01', opening_price='1.00', predicted_closing_price="1.10")    #  0.1 change
        StockPrice.objects.create(stock=stock1, date='2020-01-01', opening_price='1.00', predicted_closing_price="0.90")    # -0.1 change
        prices = StockPrice.objects.filter(stock=stock1)

        expectedStocks = [1, 1]
        expectedActions = ['hold', 'hold']
        expectedChange = [0.1, -0.1]

        # Act
        result = stock_suggestions(prices, -0.1, 0.1)
        stocks = [suggest['stock'] for suggest in result]
        actions = [suggest['action'] for suggest in result]
        change = [suggest['percent_change'] for suggest in result]

        # Assert
        self.assertEquals(stocks, expectedStocks)
        self.assertEquals(actions, expectedActions)
        self.assertAlmostEquals(float(change[0]), expectedChange[0])
        self.assertAlmostEquals(float(change[1]), expectedChange[1])

    def test_within_thresholds(self):
        # Arrange
        stock1 = Stock.objects.create(name='test1', symbol='tst1', category='testCat')
        StockPrice.objects.create(stock=stock1, date='2020-01-01', opening_price='1.00', predicted_closing_price="1.00")    #  0.0 change
        prices = StockPrice.objects.filter(stock=stock1)

        expected = [{'stock': 'tst1', 'action': 'hold', 'percent_change': 0.0},]

        # Act
        result = stock_suggestions(prices, -0.1, 0.1)

        # Assert
        self.assertEquals(result, expected)