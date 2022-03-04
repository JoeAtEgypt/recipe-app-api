from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe

from recipe import serializers


# we can refactor this code to reduce the code duplication and
# the beauty of test-driven development is that we can do this confidently
# knowing that we're not gonna break any major functionality in our code.
# TTD makes things like Refactoring and improving the code a lot easier.

class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """ Base viewset for user owned recipe attributes """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """ Return objects for the current authenticated user only """
        return self.queryset.filter(user=self.request.user).order_by('-name')

    # Overriding the "perform_create" so that we can assign the tag to the correct user.
    # "perform_create" function allows us to hook into the "create" process when creating an object.
    # what happens is when we do a "create" object in our viewset, this function will be invoked
    # and the validated serializer will be passed in, then we can perform any modifications.
    def perform_create(self, serializer):
        """ Create a new tag """
        serializer.save(user=self.request.user)

class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    """ Manage ingredients in the database """
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """ Manage Recipes in the database """
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """ Retrieve the recipe for the authenticated user """
        return self.queryset.filter(user=self.request.user)
