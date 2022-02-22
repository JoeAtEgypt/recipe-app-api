# Test 1: test that our helper function for our model can create a new user.
        # we're gonna use the "create_user" function to create a user
        # and then we're gonna to verify that user has been created as expected.
from django.test import TestCase

# You can the user model directly from the models.
# but this is not recommended with django bec. at some point in the project, you may want to change what your user model is.
# and everything is using the "get_user_model" function then that's easy to do bec. you just change it in the settings -
# instead of having to change all the references to the user model.
from django.contrib.auth import get_user_model

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """ Test creating a new user with an email is successful """
        email = 'test@joeshak.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)

        # The password is encrypted so you can only check it using the "check_password" function
        self.assertTrue(user.check_password(password))

    # A function to normalize the email address that users sign up with.
    # Not Required
    # it is recommended bec. the second part ot the user domain name for email addresses is case-insensitive. (gmail.com/outlook.com)
    def test_new_user_email_normalized(self):
        """ Test the email for a new user is normalized """
        email = 'test@LONDONAPPDEV.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ Test creating user with no email raises error """

        # what this does is anything that we run, should raise the ValueError
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """ Test creating a new superuser """
        user = get_user_model().objects.create_superuser(
            'test@joeshak.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        # "is_staff" is included in "PermissionsMixin"
        self.assertTrue(user.is_staff)






