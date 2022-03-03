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

# the account of user who is authenticated
ME_URL = reverse('user:me')

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

    # we're gonna test that authentication is required for the endpoint
    # recommended bec. authentication required on an endpoint is a quite an important part
    # bec. it affects the security of it and you don't want API's being publicly by accident
    # and a great way to prevent against that is to add Unit Test to make sure that
    # after any changes that you make those API's will always be private.
    def test_retrieve_user_unauthorized(self):
        """ Test that authentication is required for users """
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# we're gonna add some authenticated requests to our endpoint.
# So the tests that we're gonna add is the retrieve profile successful.
# the test that post is not allowed
# so we're not gonna support post in the 'ME' endpoint
# we're gonna support patch and put to update it.
# 'POST': for creating objects / "PUT"&"PATCH": for editing Objects.
class PrivateUserAPITests(TestCase):
    """ Test API requests that require authentication """

    def setUp(self):
        self.user = create_user(
            email='test@joeshak.com',
            password='testpass',
            name='name'
        )
        self.client = APIClient()
        # "force_authenticate": is a helper function that basically just make it really easy to
        # simulate or making authenticated requests.
        # So whichever request we make with this client now will be authenticated wit our sample user
        self.client.force_authenticate(user=self.user)

    # test that we can retrieve the profile of the logged-in user.
    def test_retrieve_profile_success(self):
        """ Test retrieving profile for logged-in user """
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        """ Test that POST is not allowed on the "ME" URL """
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """ Test updating the user profile for authenticated user """
        payload = {'name': 'new name', 'password': 'newpassword123'}

        res = self.client.patch(ME_URL, payload)

        # we can use the refresh from DB helper function on our user to update the user with the latest values from the database.
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)




