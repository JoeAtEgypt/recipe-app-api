from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

# "APIClient": test client that we can use to make requests to our API
    #and then check what the response is.
from rest_framework.test import APIClient
from rest_framework import status

# At the beginning of any API test that I create is I add either
# a helper function or
# a constant variable for our URL that we're gonna be testing.
CREATE_USER_URL = reverse('user:create')

# we don't need to add authentication bec. the purpose of this API is to start the authentication.
TOKEN_URL = reverse('user:token')

# "**": dynamic list of arguments. so we can basically add as many arguments as we want.
def create_user(**params):
    return get_user_model().objects.create_user(**params)

# A public API is one that is unauthenticated.
class PublicUserAPITests(TestCase):
    """ Test the users API (public) """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """ Test creating user with valid payload is successful """
        # payload is the object that you pass to the API when you make the request.
        # Test that if you pass in all correct fields then the user is created successfully.
        payload = {
            'email': 'test@joeshak.com',
            'password': 'testpass',
            'name': 'Test name'
        }
        # Making Our Request
        res = self.client.post(CREATE_USER_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        # Checking that the password is not returned as a part of "payload" object. (Security)
        self.assertNotIn('password', res.data)


    def test_user_exists(self):
        """ Test Creating a user that already exists fails """
        payload = {'email': 'test@joeshak.com', 'password': 'testpass'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload, format='json')

        # check if 400 Bad Request bec. the user already exists
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_password_too_short(self):
        """ Test that the password must be more than 5 characters """
        payload = {'email': 'test@joeshak.com', 'password':'pw'}
        res = self.client.post(CREATE_USER_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)


    ## 4 Unit Tests
        # 1. unit Test for "the token is created successfully".
        # 2. another Unit Test checks what happens if we provide invalid credentials.
        # 3. another Unit Test checks if you're trying to authenticate against a non-existent user.
        # 4. another Unit Test checks if you provide a request that doesn't include a password

    def test_create_token_for_user(self):
        """ Test that a token is created for the user """
        payload = {'email': 'test@joeshak.com', 'password': 'testpass'}
        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload, format='json')

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """ Test that token is not created if invalid credentials are given """
        create_user(email='test@joeshak.com', password='testpass')
        payload = {'email': 'test@joeshak.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload, format='json')

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """ Test that token is not created if user does not exist """
        payload = {'email': 'test@joeshak.com', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload, format='json')

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """ Test that email and password are required """
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)




