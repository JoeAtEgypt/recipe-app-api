from rest_framework import generics, authentication, permissions
# "ObtainAuthToken": this comes with Django rest framework
# so you're authenticated using a username and password as a standard.
# using this by making "ObtainAuthToken directly into our URLs"
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """ Create a new user in the system """
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """ Create a new auth token for user """
    serializer_class = AuthTokenSerializer

    # we can set our renderer class and
    # all this does is it sets the renderer class and
    # all this does is it sets the renderer so we can view this endpoint in the browser with the browsable API.
    # that means we can basically login using Chrome and
    # you can tye in the username and password and you can click post and then it should return the token
    # if you don't this, then you have to use a tool such as CURL or some other tool to basically make the HTTP POST request.
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

# Authentication is the mechanism by which the authentication happens
# so this could be cookie authentication or we're gonna use is Token Authentication

# Permission are the level of access that the user has.
# so the only permission we're gonna add is that the user must be authenticated to use this API.
# they don't have to have any special permissions, they just have to be logged-in.
class ManageUserView(generics.RetrieveUpdateAPIView):
    """ Manage the Authenticated User """
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    # we're gonna override the "get_object" and we're just gonna return the user that is authenticated.
    # So when the "get_object" is called the request will have, the user attached to it,
    # bec. of the authentication classes, is the authenticated User and assigning it to request.
    def get_object(self):
        """ Retrieve and Return Authentication User """
        return self.request.user


