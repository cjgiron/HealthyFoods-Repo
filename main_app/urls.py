from django.urls import path     
from . import views
from .views import LikeView


urlpatterns = [
    path('', views.index),
    path('login_process', views.login_process),
    path('register_process', views.register_process),
    path('dashboard', views.dashboard),
    path('add_recipe', views.add_recipe),
    path('recipe_process', views.recipe_process),
    path('recipes/<int:recipe_id>', views.display_recipe),
    path('<int:recipe_id>/edit_recipe', views.edit_recipe),
    path('<int:recipe_id>/update_recipe', views.update_recipe),
    path('<int:recipe_id>/delete', views.delete),
    path('logout', views.logout),
    path('<int:recipe_id>/follow', views.follow_recipe),
    path('<int:recipe_id>/remove', views.remove_recipe),
    path('<int:recipe_id>/process_comment', views.process_comment),
    path('<int:recipe_id>/<int:comment_id>/delete_comment', views.delete_comment),
    path('like/<int:pk>/<int:recipe_id>', LikeView, name="like_post"),
    path('search_recipes', views.search_recipes, name='search-recipes')
]