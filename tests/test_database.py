import pytest
import os
import json
from pathlib import Path
from cookbook_manager.database import JsonDatabase
from cookbook_manager.models import Recipe, Cookbook

@pytest.fixture
def cleanup_test_db():
    """Cleanup test database files after tests."""
    yield
    test_files = ['test_recipes.json', 'test_cookbooks.json']
    data_dir = Path('./data')
    for file in test_files:
        try:
            (data_dir / file).unlink(missing_ok=True)
        except:
            pass
    try:
        data_dir.rmdir()
    except:
        pass

def test_json_database_basic_operations(cleanup_test_db):
    db = JsonDatabase[Recipe]('test_recipes.json')
    
    # Test insert
    recipe = Recipe(name="Test Recipe", url="http://test.com/recipe")
    db.insert(recipe)
    
    # Test get all
    all_recipes = db.get_all()
    assert len(all_recipes) == 1
    assert all_recipes[0]['name'] == "Test Recipe"
    
    # Test find by field
    found_recipe = db.find_by_field('name', "Test Recipe")
    assert found_recipe is not None
    assert found_recipe['url'] == "http://test.com/recipe"
    
    # Test update
    updated = db.update_by_field('name', "Test Recipe", {'url': "http://new.com/recipe"})
    assert updated is True
    updated_recipe = db.find_by_field('name', "Test Recipe")
    assert updated_recipe['url'] == "http://new.com/recipe"
    
    # Test delete
    deleted = db.delete_by_field('name', "Test Recipe")
    assert deleted is True
    assert len(db.get_all()) == 0

def test_json_database_cookbook_operations(cleanup_test_db):
    db = JsonDatabase[Cookbook]('test_cookbooks.json')
    
    # Test cookbook with recipes
    recipe = Recipe(name="Pancakes", url="http://test.com/pancakes")
    cookbook = Cookbook(
        name="Breakfast Recipes",
        description="Morning recipes",
        recipes=[recipe]
    )
    
    # Test insert and retrieve cookbook
    db.insert(cookbook)
    all_cookbooks = db.get_all()
    assert len(all_cookbooks) == 1
    assert all_cookbooks[0]['name'] == "Breakfast Recipes"
    assert len(all_cookbooks[0]['recipes']) == 1
    assert all_cookbooks[0]['recipes'][0]['name'] == "Pancakes"
