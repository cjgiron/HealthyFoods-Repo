from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User, Recipe, Comment
import bcrypt
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect


def LikeView(request, pk, recipe_id):
    user = User.objects.get(id=request.session['user_id'])
    recipe = get_object_or_404(Recipe, id=request.POST.get('recipe_id'))
    recipe.likes.add(user)
    return redirect(f'/recipes/{recipe_id}')

def index(request):
    if "user_id" in request.session:
        return redirect('/dashboard')
    return render(request, "index.html")



def login_process(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        
        return redirect('/')
    else:
        user = User.objects.get(email = request.POST['email'])
        request.session['user_id'] = user.id
        return redirect('/dashboard')


def register_process(request):
    errors = User.objects.registration_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        print(pw_hash)

        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash
        )
        
        request.session['user_id'] = user.id

        return redirect('/dashboard')


def dashboard(request):
    if "user_id" not in request.session:
        return redirect('/')

    context = {
        "all_recipes": Recipe.objects.all(),
        "user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, "dashboard.html", context)


def add_recipe(request):
    return render(request, "create_recipe.html")


def recipe_process(request):

    errors = Recipe.objects.recipe_validator(request.POST)
    if len(errors) > 0:
        
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/add_recipe')

    else: 
        this_user = User.objects.get(id=request.session['user_id'])
        Recipe.objects.create(
            user = this_user,
            recipe_title = request.POST['recipe_title'],
            description = request.POST['description'],
            ingredients = request.POST['ingredients'],
            directions = request.POST['directions'],
            prep_time = request.POST['prep_time'],
            cook_time = request.POST['cook_time'],
            num_of_servings = request.POST['num_of_servings'],
        )

        return redirect('/dashboard')


def display_recipe(request, recipe_id):
    stuff = get_object_or_404(Recipe, id=recipe_id)
    total_likes = stuff.total_likes()
    context = {
        'recipe': Recipe.objects.get(id=recipe_id),
        'user': User.objects.get(id=request.session['user_id']),
        'total_likes': total_likes
    }
    return render(request, "display_recipe.html", context)


def edit_recipe(request, recipe_id):
    context = {
        'recipe': Recipe.objects.get(id=recipe_id)
    }
    return render(request, "edit.html", context)


def update_recipe(request, recipe_id):
    print(request.POST)
    errors = Recipe.objects.recipe_validator(request.POST)
    if len(errors) > 0:
        
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/{recipe_id}/edit_recipe')
    
    else:
        this_recipe = Recipe.objects.get(id=recipe_id)
        title = request.POST['recipe_title']
        print(title)
        print('********************')
        this_recipe.recipe_title = title
        this_recipe.description = request.POST['description']
        this_recipe.ingredients = request.POST['ingredients']
        this_recipe.directions = request.POST['directions']
        this_recipe.prep_time = request.POST['prep_time']
        this_recipe.cook_time = request.POST['cook_time']
        this_recipe.num_of_servings = request.POST['num_of_servings']
        this_recipe.save()

    return redirect('/dashboard')


def delete(request, recipe_id):
    this_recipe = Recipe.objects.get(id=recipe_id)

    this_recipe.delete()
    return redirect('/dashboard')


def logout(request):
    request.session.flush()
    return redirect('/')


def follow_recipe(request, recipe_id):
    this_recipe = Recipe.objects.get(id=recipe_id)
    this_user = User.objects.get(id=request.session['user_id'])

    this_user.recipes_followed.add(this_recipe)
    return redirect('/dashboard')


def remove_recipe(request, recipe_id):
    this_recipe = Recipe.objects.get(id=recipe_id)
    this_user = User.objects.get(id=request.session['user_id'])

    this_user.recipes_followed.remove(this_recipe)
    return redirect('/dashboard')


def process_comment(request, recipe_id):
    print(request.POST)
    errors = Comment.objects.comment_validator(request.POST)
    if len(errors) > 0:
        
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/recipes/{recipe_id}')
    
    else:
        Comment.objects.create(
            user = User.objects.get(id=request.POST['user_id']),
            text = request.POST['text'],
            recipe = Recipe.objects.get(id=recipe_id)
        )
        return redirect(f'/recipes/{recipe_id}')


def delete_comment(request, recipe_id, comment_id):
    this_comment = Comment.objects.get(id=comment_id)

    this_comment.delete()
    return redirect(f'/recipes/{recipe_id}')