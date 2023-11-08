from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser  # Import your User model
from .serializers import UserSerializer  # Import your User serializer
from .views import UserRegistrationView  # Import your User registration view

class UserRegistrationTests(APITestCase):
    def test_successful_registration(self):
        url = reverse('register')  # Replace with your actual URL name
        data = {
            'email': 'testuser@example.com',
            'password': 'mypassword',
            # Add other required data for registration
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        user = CustomUser.objects.get()
        self.assertEqual(user.email, 'testuser@example.com')
        # Add more assertions for user data and success message if needed

    def test_registration_with_invalid_referrer_code(self):
        url = reverse('register')  # Replace with your actual URL name
        data = {
            'email': 'testuser@example.com',
            'password': 'mypassword',
            'referrer_code': 'invalid_code',  # An invalid referrer code
            # Add other required data for registration
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Add more assertions to check the response message and other details

    def test_registration_with_valid_referrer_code(self):
        # Create a user with a valid referrer code
        referrer = CustomUser.objects.create_user(email='referrer@example.com', password='referrerpassword')
        referrer.referral_code = 'valid_referrer_code'
        referrer.save()

        url = reverse('register')  # Replace with your actual URL name
        data = {
            'email': 'testuser@example.com',
            'password': 'mypassword',
            'referrer_code': 'valid_referrer_code',  # A valid referrer code
            # Add other required data for registration
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)  # Check that a new user is created
        user = CustomUser.objects.get(email='testuser@example.com')
        self.assertEqual(user.referred_by, referrer)  # Check that the referrer is correctly set
        self.assertEqual(referrer.referral_balance, Decimal(1000.00))  # Check that the referrer's balance is updated

    # Additional test cases can be added as needed

    def test_registration_failure(self):
        # Simulate a failure scenario in your view and test for it
        # For example, by raising an exception in your view
        # Then check that the response status is 500

        url = reverse('register')  # Replace with your actual URL name
        data = {
            'email': 'testuser@example.com',
            'password': 'mypassword',
            # Add other required data for registration
        }

        # Inject a scenario that causes a failure in the view
        # For example, by mocking a dependency that raises an exception

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        # Add more assertions if needed

    def test_registration_validation_error(self):
        url = reverse('register')  # Replace with your actual URL name
        data = {
            # Omit required fields to trigger validation errors
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Add more assertions to check the response data and error messages

    def test_registration_with_existing_email(self):
        # Create a user with the same email as the one you're trying to register
        CustomUser.objects.create_user(email='testuser@example.com', password='mypassword')

        url = reverse('register')  # Replace with your actual URL name
        data = {
            'email': 'testuser@example.com',
            'password': 'mypassword',
            # Add other required data for registration
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Add more assertions to check the response message
