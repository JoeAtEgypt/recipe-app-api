# Test 1: test that our helper function for our model can create a new user.
# we're gonna use the "create_user" function to create a user
# and then we're gonna to verify that user has been created as expected.
from django.test import TestCase

from unittest.mock import patch

# You can the user model directly from the models.
# but this is not recommended with django bec. at some point in the project, you may want to change what your user model is.
# and everything is using the "get_user_model" function then that's easy to do bec. you just change it in the settings -
# instead of having to change all the references to the user model.
from django.contrib.auth import get_user_model
from .. import models


def sample_user(email='test@joeshak.com', password='testpass'):
    """ Create a sample user """
    return get_user_model().objects.create_user(email, password)


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

    def test_tag_str(self):
        """Test the tag string representation """
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )
        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """ Test the ingredient string representation """
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name="Cucumber"
        )
        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """ Test the recipe string representation """
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and mushroom sauce',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)

    # 'uuid4' = is a function within the 'uuid' module which will generate a unique 'uuid' version 4
    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        # that means anytime we call this uuid4 function that is
        # triggered from within our test, it will change the value, override the default behaviour
        # and return 'uuid' instead; this allows us to reliably test how our function works.
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid

        # 'recipe_image_file_path': it accepts 2 parameters
        # 1. an instance
        # 2. the file name of the original file which is being added.
        # the reason we passed 'myimage.jpg' in bec. what we're gonna do is
        # we're gonna remove this image part 'myimage' and replace it with the 'uuid' but we wanna kep the extension;
        # as it maintains whatever file type is uploaded.
        # so you can upload JPEGs or PNGs and so on.
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
