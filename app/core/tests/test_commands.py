## Mocking
    # when you override or change the behaviour of the dependencies of the code that you're testing.
    # used in:
        # 1. avoid any unintended side-effects.
        # 2. isolate the specific piece of code that we want to test.

    # for Example: Imagine you're testing a function that sends an email.
        # there are 2 good reasons that you wouldn't want to actually send an email every time you run your tests.
            # 1st Reason: you should never write tests that depend on external services.
                # bec. you can't guarantee that these services will available at the point that you run a test.
                # and this will make the tests unpredictable and unreliable.
            # 2nd Reason: you don't want to be sending spam emails each time you run your test suite
                # even if you're a fake address, those emails would still be backing up on a server somewhere.

        # when you write your test, you can use "Mocking" to avoid sending an actual email.
        # You can override the function in the dependency that sends the email and replace it with a Mock Object.
        # Using this Mock Object, we can avoid sending an actual email
        # and instead just check that the function was called with the correct parameters.

## Adding a management command:
    # is a helper command that allows us to wait for the database to be available before continuing and adding other commands.
    # the reason we need this command is bec. I find that sometimes when using Postgresql with docker compose in a django app,
    # sometimes the django app fails to start bec. of database error.
    # it turns out that this is bec. on the postgres services has started,
    # there are a few extra setup tasks that need to be done on the postgres before it is ready to accept connections.
        # what this means is that our django app will try and connect to our database before database is ready
        # and therefore it will fail with an exception and you will need to restart the app.

    # this will make our app a lot more reliable when running it locally as a development server
    # and also if we ever deploy it as a production system.




# Patch Function:
        # allows us to mock the behaviour of the Django get database function.
        # it basically simulate the database being available and not being available for when we test our command.
from unittest.mock import patch

# Call Command Function:
        # allows us to call the command in our source code.
from django.core.management import call_command

# Operational Error: that Django throws when tha database is unavailable.
        # simulates the database being available or not when we run our command.
from django.db.utils import OperationalError

from django.test import TestCase


class CommandTests(TestCase):

    # test what happens when we call our command and the database is already available.
    def test_wait_for_db_ready(self):
        """ Test waiting for db when db is available """

        # to setup our test, we need to simulate the behaviour of Django when the database is available.
            # Our Management command is gonna basically try and retrieve the database connection from Django.
            # and it's gonna check if when we try and retrieve it, it retrieves an Operational Error or not.
        # to setup our test, we're gonna override the behaviour of the "ConnectionHandler"
        # and make it return true and not throw any exception and then Our Management commands should continue and allows us to continue with the execution flow.

        # let's use the "patch" to mock the "ConnectionHandler" to just return true every time it's called.
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # the way that we tested the database is available in Django is
                # we just try and retrieve the default database via "ConnectionHandler" function '__getitem__'.
            # So we're gonna mock the behaviour of this "__getitem__" Using "patch" which is assigned as a variable "gi".

            # whenever "getitem" is called during our test execution instead of actually before performing whatever behaviour of this function does in Django,
            # it will override it and replace it with a mock object which does 2 things:
                # 1. specify "return_value"
                # 2. allow us to monitor how many times it was called and the different calls that were made to it.
            gi.return_value = True

            # test our call_command
            # "wait_for_db" is gonna be the name of management command that we create.
            call_command('wait_for_db')

            # all we're gonna check is that "__getitem__" was called once.
            self.assertEqual(gi.call_count, 1)

    # what this does: it replaces the behaviour of "time.sleep" and replaces it with a mock function that returns true.
    # the reason with this is to speed up the test when you run them.
    # bec. if we're checking the database 5 times, then that is 5 extra seconds that it would take to run our tests.
    # "ts" = "gi" (Mock Object), it must be passed in as an extra argument; Otherwise it will show a test error.
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):    # Test if "wait_for_db" command will try database 5 times and then on the 6th time, it'll be successful and it will continue.
        """ Test waiting for db """
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:

            # Adding a SideEffect
            # The Python Unit Tests Mock Module has a really useful option where you can set a side effect to
            # the function that you're mocking.

            # SideEffect: Raise The Operational Error 5 times, and then on 6th time, it's not gonna raise the error and then the call should complete.
            # "[OperationalError] * 5": means you call this "__getitem__", Raise the Operational Error
            # "+ [True]": means that in the additional 6th time, it won't raise the error, it will just return.
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)





