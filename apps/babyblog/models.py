from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import bcrypt, re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate_reg(self, request):
        errors = self.validate_inputs(request)

        if errors:
            return (False, errors)

        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

        user = self.create(user_name=request.POST['user_name'], email=request.POST['email'], password=pw_hash)

        return (True, user)

    def validate_login(self, request):
        try:
            user = User.objects.get(email=request.POST['email'])
            password = request.POST['password'].encode()
            if bcrypt.hashpw(password, user.password.encode()):
                return (True, user)

        except ObjectDoesNotExist:
            pass

        return (False, ["Invalid login."])

    def validate_inputs(self, request):
        errors = []

        if not request.POST['user_name']:
            errors.append('Username cannot be blank.')
        if not EMAIL_REGEX.match(request.POST['email']):
            errors.append('Invalid email.')
        if request.POST['password'] < 8:
            errors.append('Password must be at least 8 characters.')
        if request.POST['password'] != request.POST['confirm']:
            errors.append('Password and password confirm must match.')

        return errors

class TweetManager(models.Manager):
    def post_tweet(self, request):
        errors = []

        if not request.POST['new_tweet']:
            errors.append('Please write a Baby Tweet!')

        else:
            creator = User.objects.get(id=request.session['user']['user_id'])
            self.create(content=request.POST['new_tweet'], tweet_creator=creator)

        return errors

    def destroy_tweet(self, request, id):
        Tweet.objects.filter(id=id).delete()


class User(models.Model):
    user_name = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Tweet(models.Model):
    content = models.CharField(max_length = 70)
    tweet_creator = models.ForeignKey(User, related_name = 'user_tweet')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TweetManager()
