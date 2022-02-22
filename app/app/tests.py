# # The Django Unit Test Framework looks for any files that begin with "tests"
# # and basically uses them as the tests when you run Django, Run unit tests command
#
# # the "TestCase" is a class that comes with Django that basically
# # has a bunch of helper functions that help us test our Django code.
# from django.test import TestCase
#
# from .calc import add, subtract
#
#
# class CalcTests(TestCase):
#
#     # the test functions must all begin with "test". if not, it wouldn't run this test but Django test (Default)
#     def test_add_numbers(self):
#         # in the test, we'll just always start a test with a description of what you're testing.
#         """ Test that 2 numbers are added together """
#
#         # a Test is set up of 2 components:
#             # 1. A setUp Stage: where you would set your function up to be tested.
#             # 2. n Assertion: where you actually test the output and you confirm that the output = you expected it.
#         self.assertEqual(add(3,8), 11)
#
# ## Test-driven Development
#     # it is simply when you write the test before you write the code.
#     def test_subtract_numbers(self):
#         """ Test that values are subtracted and returned """
#         self.assertEqual((subtract(5, 11)), 6)
#
#
#
