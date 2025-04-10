import pytest
from cookbook_manager.models import Recipe, Cookbook

def test_create_recipe():
    recipe = Recipe(
        name="Classic Pancakes",
        url="https://example.com/recipes/pancakes"
    )
    assert recipe.name == "Classic Pancakes"
    assert recipe.url == "https://example.com/recipes/pancakes"

def test_create_cookbook():
    cookbook = Cookbook(
        name="Breakfast Favorites",
        description="Collection of breakfast recipes"
    )
    assert cookbook.name == "Breakfast Favorites"
    assert cookbook.description == "Collection of breakfast recipes"
    assert len(cookbook.recipes) == 0

def test_cookbook_add_recipe():
    recipe = Recipe(
        name="Classic Pancakes",
        url="https://example.com/recipes/pancakes"
    )
    cookbook = Cookbook(
        name="Breakfast Favorites",
        description="Collection of breakfast recipes",
        recipes=[recipe]
    )
    assert len(cookbook.recipes) == 1
    assert cookbook.recipes[0].name == "Classic Pancakes"
