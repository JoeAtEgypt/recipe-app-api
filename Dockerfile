# 1st line of this file is the image that you're gonna inherit your docker file from.
# with Docker, you can basically build images on top of other images.
        # the benfit of this is that you can find an image that has pretty much everything that you need your project
        # and then you can just add the customized bits that you need just for your specific product.

# From Docker Hub
FROM python:3.7-alpine
# Apline Image is very light-weight and minimal image that runs python

# the next line : Maintainer Line [OPTIONAL]
MAINTAINER Joe Web Developer


# Next: we're gonna set the python unbuffered environment variable
# what this does is that it tells python to run in unbuffered mode
# which is recommended when running Python within Docker Containers because it doesn't allow Python to buffer the outputs.
# it prints them directly. and this avoid some complications with thd docker image when you're running your Python App.
ENV PYTHONUNBUFFERED 1

# Next: we're gonna install our dependencies
# we're gonna store our dependencies in "requirements.txt" list
# what this does is it says copy, from dir adjacent to Docker file(LOCAL),
# the "requirements.txt" on the docker image to "requirements.txt"
COPY ./requirements.txt /requirements.txt

# what this does is it takes the requirements file that we've just copied and its installs it
RUN pip install -r /requirements.txt

# Next: we're gonna make a dir within our Docker Image that we can use to store our app source code.
RUN mkdir /app
# what this does is t creates an empty folder on our docker image called "app"

WORKDIR /app
# and then it switches to that as the default dir.
# So any app we run, using our docker container, will run starting from this location unless we specify otherwise.

COPY ./app /app
# then what it does is it copies from our local machine "app" folder to "app" folder that we've created on an image.
# This allows us to take the code that we cray in our products and copy it into our Docker image.

# Next: we're gonna create a user that is gonna run our app using docker. (username="user")
RUN adduser -D user
# what this does is it creates a user (-D) => that is gonna be used for running apps only.

# finally we're gonna switch docker to that user.
USER user
# the reason is for Security Purposes: if you create user just for our app, then this kind of limits (the scope) an attacker would have in our documentation.
# if we don not do this, then tha image will run our app using the root account
# which is not recommended bec. that means if sb. compromises our app, the have root access to tha whole image.



## Commands
# 1. "docker build ."
    # => what it does is its says build whichever docker file is in the roout dir of our project that we 're currently in.
    # the reason we call it "Dockerfile" is bec. this is the standard convention the docker uses to identify the docker file within our project.
# 2. "docker-compose run app"
    # => we're gonna run the command on the app
    # and anything after this command is gonna be the command that get run on the linux container that we created using our docker file.