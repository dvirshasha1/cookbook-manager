"""Tests for the CookbookManager class."""
import pytest
from cookbook_manager.app import CookbookManager
from cookbook_manager.models import Recipe, Cookbook
from unittest.mock import MagicMock

@pytest.fixture
def manager():
    """Create a CookbookManager instance with mocked databases."""
    manager = CookbookManager()
    manager.cookbook_db = MagicMock()
    manager.recipe_db = MagicMock()
    return manager

@pytest.fixture
def sample_recipe():
    """Create a sample recipe for testing."""
    return Recipe(name="Test Recipe", url="http://test.com/recipe")

@pytest.fixture
def sample_cookbook(sample_recipe):
    """Create a sample cookbook with one recipe for testing."""
    return Cookbook(
        name="Test Cookbook",
        description="Test Description",
        recipes=[sample_recipe]
    )

def test_add_cookbook(manager):
    """Test adding a cookbook."""
    cookbook = manager.add_cookbook("Test Cookbook", "Test Description")
    manager.cookbook_db.insert.assert_called_once()
    assert cookbook.name == "Test Cookbook"
    assert cookbook.description == "Test Description"

def test_get_all_cookbooks(manager, sample_cookbook):
    """Test retrieving all cookbooks."""
    cookbook_data = [sample_cookbook.model_dump()]
    manager.cookbook_db.get_all.return_value = cookbook_data
    
    cookbooks = manager.get_all_cookbooks()
    assert len(cookbooks) == 1
    assert cookbooks[0].name == "Test Cookbook"
    manager.cookbook_db.get_all.assert_called_once()

def test_get_cookbook_by_name(manager, sample_cookbook):
    """Test retrieving a cookbook by name."""
    cookbook_data = sample_cookbook.model_dump()
    manager.cookbook_db.find_by_field.return_value = cookbook_data
    
    cookbook = manager.get_cookbook_by_name("Test Cookbook")
    assert cookbook.name == "Test Cookbook"
    manager.cookbook_db.find_by_field.assert_called_once_with('name', 'Test Cookbook')

def test_delete_cookbook(manager):
    """Test deleting a cookbook."""
    manager.cookbook_db.delete_by_field.return_value = True
    assert manager.delete_cookbook("Test Cookbook") is True
    manager.cookbook_db.delete_by_field.assert_called_once_with('name', 'Test Cookbook')

def test_add_recipe(manager):
    """Test adding a recipe."""
    recipe = manager.add_recipe("Test Recipe", "http://test.com/recipe")
    manager.recipe_db.insert.assert_called_once()
    assert recipe.name == "Test Recipe"
    assert recipe.url == "http://test.com/recipe"

def test_add_recipe_to_cookbook(manager, sample_cookbook, sample_recipe):
    """Test adding a recipe to a cookbook."""
    cookbook_data = sample_cookbook.model_dump()
    recipe_data = sample_recipe.model_dump()
    
    manager.cookbook_db.find_by_field.return_value = cookbook_data
    manager.recipe_db.find_by_field.return_value = recipe_data
    
    result = manager.add_recipe_to_cookbook("Test Cookbook", "Test Recipe")
    assert result is True
    manager.cookbook_db.update_by_field.assert_called_once()
