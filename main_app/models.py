from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def registration_validator(self, post_data):
        errors = {}

        # validate names
        if len(post_data['first_name']) < 2:
            errors['first_name'] = "First name should be longer than two characters."
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last name should be longer than two characters."

        # validate email
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        else:
            user_list = User.objects.filter(email = post_data['email'])
            if len(user_list) > 0:
                errors['email'] = "Email already in use."

        # validate password
        if len(post_data['password']) < 8:
            errors['password'] = "Password should be longer than 4 characters."
        if post_data['password'] != post_data['confirm_password']:
            errors['confirm_password'] = "Password and Confirm PW must match."
        return errors


    def login_validator(self, post_data):
        errors = {}

        user_list = User.objects.filter(email = post_data['email'])
        if len(user_list) > 0:
            user = user_list[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors['password'] = "Invalid Credentials"
        else:
            errors['email'] = "Invalid Credentials"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class RecipeManager(models.Manager):
    def recipe_validator(self, post_data):
        errors = {}

        if len(post_data['recipe_title']) < 2:
            errors['recipe_title'] = "Title must be longer than 2 characters."

        if len(post_data['description']) < 10:
            errors['description'] = "Description must be at least 10 characters long."

        if len(post_data['ingredients']) < 10:
            errors['ingredients'] = "Ingredients must be at least 10 characters long."

        if len(post_data['directions']) < 10:
            errors['directions'] = "Directions must be at least 10 characters long"

        if len(post_data['prep_time']) < 1:
            errors['prep_time'] = "Enter a prep time."

        if len(post_data['cook_time']) < 1:
            errors['cook_time'] = "Enter a cook time."

        if post_data['num_of_servings'] == "":
            errors['num_of_servings'] = "Enter number of servings."
        return errors


class Recipe(models.Model):
    user = models.ForeignKey(User, related_name="recipes", on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name="recipes_followed")
    recipe_title = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.TextField()
    directions = models.TextField()
    prep_time = models.CharField(max_length=255)
    cook_time = models.CharField(max_length=255)
    num_of_servings = models.IntegerField()
    likes = models.ManyToManyField(User, related_name="recipes_liked")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = RecipeManager()

    def total_likes(self):
        return self.likes.count()

class CommentManager(models.Manager):
    def comment_validator(self, post_data):
        errors = {}

        if len(post_data['text']) < 5:
            errors['text'] = "Comment must be longer than 5 characters."
        return errors


class Comment(models.Model):
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name="recipe_comments", on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()