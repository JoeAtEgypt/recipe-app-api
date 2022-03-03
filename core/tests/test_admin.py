# "client": allows us to make requests to our pp in our unit tests.
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    #  function that is ran before every test that we run. So sometimes there are setup tasks that need to be done before every test in our "TestCase" class.
    def setUp(self):
        # Our "setUp" consists of creating our test client
        # adding a new user that we can use to test
        # making sure tha user is logged into our client
        # Finally, creating a regular user that is not authenticated or that is listed in our admin panel.

        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='az@az.com',
            password='12345'
        )

        # what this does is it uses the "Client" helper function that allows you to log a user in with Django authentication.
        # and that makes our tests a lot easier to write bec. it means we don't have to manually log the user in.
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email="test@joeshak.com",
            password="test123",
            name='Test user full name'
        )

    # Text that the users are listed in our Django Admin
    # Bec. we need to slightly customize the Django admin to work with our custom user model.
    def test_users_listed(self):
        """ Test that users are listed on the user page """

        # what this does is it generates the URL for list user page
        # The reason we use "reverse" function instead of typing URL manually is bec. if we ever want to change The URL,
                # it means we don't have to go through and change it everywhere in our test.
                # bec. it should update automatically based on "reverse".
        url = reverse('admin:core_user_changelist')

        # shortening Response bec. it makes the test a bit cleaner otherwise you have lots of long lines in your code.
        res = self.client.get(url)

        # "assertContains" assertion:
                # a Django Custom Assertion that will check that our response contain a certain item ("user.name" or "user.email")
                # 2. it checks that the HTTP response was HTTP 200(OK)
                # 3. it looks into the actual content of this "res" bec. if we were to manually output this "res"(just an object)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """ Test that the user edit page works """

        # what this does is the "reverse" function will create a URL.
        # args = id in this URL
        # /admin/core/user/1
        url = reverse('admin:core_user_change', args=[self.user.id])

        res= self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """ Test that the create user page works """
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)



