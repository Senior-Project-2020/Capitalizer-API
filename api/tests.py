from django.test import TestCase
from .models import PCUser, Interest

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