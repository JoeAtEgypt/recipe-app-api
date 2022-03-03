# 1st line of this file is the image that you're gonna inherit your docker file from.
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

WORKDIR /recipe-app-api

# Next: we're gonna install our dependencies
# we're gonna store our dependencies in "requirements.txt" list
# what this does is it says copy, from dir adjacent to Docker file(LOCAL),
# the "requirements.txt" on the docker image to "requirements.txt"
COPY requirements.txt /recipe-app-api/

# installing the postgreSQL client
# it uses the package manager "apk" that comes with alpine
# "add" = add a package
# "--update" = update the registry before we add it.
# "--no-cache" = on not store the registry index on our docker file bec. we really wanna minimize #extra files and packages that ar included in our docker container.
# this is the best practice bec. it means that your docke container for your app has the smallest footprint possible
# and also means that you don't include any extra dependencies or anything on your system which may cause unexpected side effects or make Security Vulnerabilities in your system.
RUN apk add --update --no-cache postgresql-client

# installing Temporary packages that need to be installed on the system while we run our "requirements.txt"
# and then we can remove them after "requirements.txt" has run.
# "--virtual" = sets up an alias for our dependencies that we can use to easily remove all those dependencies later.
# ".tmp-build-deps" = Tempoary Build Dependencies
# "gcc, libc-dev, linux-headers postgresql-dev" = Temporary dependencies.
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev

# what this does is it takes the requirements file that we've just copied and its installs it
RUN pip install -r requirements.txt

# delete all temporary Dependencies.
RUN apk del .tmp-build-deps

COPY . /app
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
# 3. "docker-compose run -rm app sh -c "python manage.py startapp user" "
    # => "-rm": you can include this optionally on any commands that you want to run once and
              # you don't want the docker container to linger on the system after it's ran.
              # it removes the container and just keep the system a little cleaner so it doesn't fill up.

## Notes:
    # 1. the Packagethat Django recommends for communicating between Django and POSTGRES is called "psycopg2"