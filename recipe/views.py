from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
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

    # Python doesn't have the concept of public and private functions.
    # All functions are public functions.
    # however what you can do is to provide an '_' before the name of the function
    # this is the common convention when you wanna indicate that a function is intended to
    # be private as you will still be able to call it as a public function.
    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """ Retrieve the recipe for the authenticated user """
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            # 'tags__id__in': thi is the Django syntax for filtering on foreign key objects.
            # '__in': this is a function called 'in' in which basically says return all of
            # tags where the ID is in this list that we provide 'tags_ids'.
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.filter(user=self.request.user)

    # this is a function that's called to retrieve the serializer class for a particular request.
    def get_serializer_class(self):
        """ Return appropriate serializer class """
        # "action" class variable which will contain the action that is being used for our current request
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        if self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """ Create a new recipe """
        serializer.save(user=self.request.user)

    # Now you define actions as functions in the viewset by default.
    # It has these 'get_queryset', 'get_serializer_class', and 'perform_create', these are all
    # default actions that we override so if we didn't override them then they will just perform
    # the default action that the Django rest framework does.
    # You can actually add Custom Action
    # the way to add this is to use the '@action' decorator
    # then you define the methods that your action is gonna accept, so the methods could be:
    # POST, PUT, PATCH or GET.
    # 'detail=True'= this means that the action will be for the detail
    # the detail is a specific recipe detail
    # 'url_path': that will be the path that is visible within the URL
    # it will be 'recipe/id/upload-image'
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """ Upload an image to a recipe """

        # 'get_object': will get the default or the object that is being accessed based on the ID in the URL.
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


