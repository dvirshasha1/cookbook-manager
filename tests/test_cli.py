import pytest
from unittest.mock import patch, MagicMock, call
from cookbook_manager.cli import CookbookCLI
from cookbook_manager.models import Recipe, Cookbook

@pytest.fixture
def cli():
    """Create a CLI instance with mocked databases for testing."""
    cli = CookbookCLI()
    cli.cookbook_db = MagicMock()
    cli.recipe_db = MagicMock()
    return cli

@pytest.fixture
def sample_recipe():
    return Recipe(name="Test Recipe", url="http://test.com/recipe")

@pytest.fixture
def sample_cookbook(sample_recipe):
    return Cookbook(
        name="Test Cookbook",
        description="Test Description",
        recipes=[sample_recipe]
    )

@pytest.fixture
def mock_pick(mocker):
    """Mock the pick function for all tests"""
    return mocker.patch('cookbook_manager.cli.pick')

def test_add_cookbook(cli, mock_pick):
    """Test adding a new cookbook."""
    # Mock user inputs including the continue prompt
    with patch('builtins.input', side_effect=["Test Cookbook", "Test Description", ""]), \
         patch('builtins.print'):  # Suppress print statements
        cli._add_cookbook()
    
    # Verify cookbook was added with correct data
    cli.cookbook_db.insert.assert_called_once()
    called_cookbook = cli.cookbook_db.insert.call_args[0][0]
    assert called_cookbook.name == "Test Cookbook"
    assert called_cookbook.description == "Test Description"

def test_view_cookbook_details(cli, sample_cookbook):
    """Test viewing cookbook details."""
    # Mock print and suppress input
    with patch('builtins.print') as mock_print, \
         patch('builtins.input', return_value=""):
        cli._view_cookbook_details(sample_cookbook)
    
    # Verify correct information was displayed
    expected_calls = [
        call("\nCookbook: Test Cookbook"),
        call("Description: Test Description"),
        call("\nRecipes:"),
        call("- Test Recipe")
    ]
    assert mock_print.call_args_list == expected_calls

def test_delete_cookbook(cli, sample_cookbook):
    """Test deleting a cookbook."""
    # Setup mock return value
    cli.cookbook_db.delete_by_field.return_value = True
    
    # Mock print and suppress input
    with patch('builtins.print'), \
         patch('builtins.input', return_value=""):
        result = cli._delete_cookbook(sample_cookbook)
    
    # Verify deletion
    cli.cookbook_db.delete_by_field.assert_called_once_with('name', 'Test Cookbook')
    assert result is True

def test_add_recipe_to_cookbook(cli, sample_cookbook, sample_recipe, mock_pick):
    """Test adding a recipe to a cookbook."""
    # Setup mock data
    cookbook_data = sample_cookbook.model_dump()
    cli.cookbook_db.find_by_field.return_value = cookbook_data
    cli.recipe_db.get_all.return_value = [sample_recipe.model_dump()]
    
    # Mock recipe selection
    mock_pick.return_value = (sample_recipe.name, 0)
    
    # Mock print and suppress input
    with patch('builtins.print'), \
         patch('builtins.input', return_value=""):
        cli._add_recipe_to_cookbook(sample_cookbook)
    
    # Verify cookbook update
    cli.cookbook_db.update_by_field.assert_called_once()

def test_main_menu(cli, mock_pick):
    """Test main menu navigation"""
    # Setup menu selection sequence
    mock_pick.side_effect = [
        ('Exit', 2)  # Select Exit option
    ]
    
    # Run main menu
    with patch('builtins.print'):
        cli.main_menu()
    
    # Verify pick was called with correct options
    mock_pick.assert_called_once()
