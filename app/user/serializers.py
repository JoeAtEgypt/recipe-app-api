# "authenticate": Django helper command for working with the Django Authentication System
                # So you simply pass in the username and password
                # and you can authenticate a request
from django.contrib.auth import get_user_model, authenticate
# whenever you're outputting any messages in the Python code that are gonna be output to the screen.
# It's a good idea to pass them through this translation system.
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers



class UserSerializer(serializers.ModelSerializer):
    """ Serializer for the user object """

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        # this allows us to configure a few extra settings in our Model Serializer
        # what we're gonna use this for is to ensure that the password is write only
        # and that the minimum required length is 5 characters.
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """ Create a new user with encrypted password and return it """

        # "validated_data": will contain all of the data that was passed into our serializer
                          # which would be the JSON data that was made in the HTTP POST
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """ Serializer for the user authentication object """
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )


    # "validate": it's called when we validate our serializer
    # the validation is basically checking that the inputs are all correct.
    # And as a part of the validation function, we also gonna validate that the authentication credentials are correct.

    # "attrs": this parameter is basically just every field that makes up our serializer.
    def validate(self, attrs):
        """ Validate and Authenticate the user """
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            # this is how you basically access the context of the request that was made.
            # so we're gonna pass this into our viewset
            # what django rest framework view set does is when a request is made,
            # it passes the context into the serializer in this "context" variable
            # and from that we can get hold of the request that was made.
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials')
            # what this does is it raises the validation error and
            # then the Django rest framework knows how to handle this error and
            # it handles it by passing the error as a 400 Response
            # and sending a response to the user which describes this message.
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
