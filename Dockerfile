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
ENV PYTHONDONTWRITEBYTECODE 1

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
# & Also Pillow Package requires some Linux packages to be installed before we can successfully compile
# and install it using the "pip" package manager.
# "jbeg-dev" adds the JBEG dev binaries to our docker file
RUN apk add --update --no-cache postgresql-client jpeg-dev

# installing Temporary packages that need to be installed on the system while we run our "requirements.txt"
# and then we can remove them after "requirements.txt" has run.
# "--virtual" = sets up an alias for our dependencies that we can use to easily remove all those dependencies later.
# ".tmp-build-deps" = Tempoary Build Dependencies
# "gcc, libc-dev, linux-headers postgresql-dev" = Temporary dependencies.
# "musl-dev", "zlib", "zlib-dev" = I retrieved these packages from the "PYPI" page for the pillow dependencies.
            # so it outlines all the dependencies that you need to have installed before you can install requirement
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev \
    freetype-dev fribidi-dev harfbuzz-dev jpeg-dev lcms2-dev \
    openjpeg-dev tcl-dev tiff-dev tk-dev

# what this does is it takes the requirements file that we've just copied and its installs it
 RUN pip install -r requirements.txt

# delete all temporary Dependencies.
RUN apk del .tmp-build-deps

COPY . /app
# then what it does is it copies from our local machine "app" folder to "app" folder that we've created on an image.
# This allows us to take the code that we cray in our products and copy it into our Docker image.

# Next we're gonna make some changes to the file structure.
# we have a place where we can store the "static" and "media" files within our container without getting any permission errors

# I'd like to store any files that may need to be shared with other containers in subdir "vol"(volume),
# this way we know where all of the volume mappings need to be in our container
# if we need to share this data with other containers in our service.
# For Example, if you had "nginx" or a web server that neede to serve these media files, you know that you'd need to map
# this "vol" and share it with web server container.
# "-p": make all of the subdirs including the dir that we need.
      # if "vol" dir doesn't exist, it will create "vol/web/media".
      # if we don't include this, then it will say sth. like the "vol" dir doesn't exist, then it'll give an error.
RUN mkdir -p /vol/web/media

# In Django, you typically have 2 files that hold static data:
# 1. "static": is typically used for things like JS, CSS files or
             # any static files that you may want to serve which are not typically changing during
# 2. "media": is typically used for any media files that are uploaded by the user. That's where we stores our images.
RUN mkdir -p /vol/web/static


# Next: we're gonna create a user that is gonna run our app using docker. (username="user")
RUN adduser -D user
# what this does is it creates a user (-D) => that is gonna be used for running apps only.

# we're gonna change the ownership of these files to the user that we've added,
# it's very important that we do this before we switch to the user because once we switch to the user,
# it can't add itself, it can't give itself permissions to view or access these files we need to give it
# while we're still running as the root user which is before we switch to the user "user".
# "-R" = means Recursive so instead of just setting the "vol" permissions, it will set any subdirs in the "vol" folder.
RUN chown -R user:user /vol/

# what that means is that thae user can do everything so the owner can do everything with the dir
# and the rest can read and exceute from the dir
RUN chmod -R 755 /vol/web

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