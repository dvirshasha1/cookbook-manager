import pytest
from unittest.mock import patch, MagicMock, call
from cookbook_manager.cli import CookbookCLI
from cookbook_manager.models import Recipe, Cookbook

@pytest.fixture
def cli():
    """Create a CLI instance with a mocked CookbookManager."""
    cli = CookbookCLI()
    cli.manager = MagicMock()
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

def test_view_all_cookbooks(cli, sample_cookbook):
    """Test viewing all cookbooks."""
    cli.manager.get_all_cookbooks.return_value = [sample_cookbook]
    
    with patch('builtins.print') as mock_print, \
         patch('builtins.input', return_value=""):
        cli._view_all_cookbooks()
    
    cli.manager.get_all_cookbooks.assert_called_once()
    mock_print.assert_any_call("\nAvailable Cookbooks:")
    mock_print.assert_any_call(f"- {sample_cookbook.name}")

def test_add_cookbook(cli):
    """Test adding a cookbook."""
    with patch('builtins.input', side_effect=["Test Cookbook", "Test Description", ""]), \
         patch('builtins.print'):
        cli._add_cookbook()
    
    cli.manager.add_cookbook.assert_called_once_with(
        "Test Cookbook", 
        "Test Description"
    )

def test_view_cookbook_details(cli, sample_cookbook):
    """Test viewing cookbook details."""
    with patch('builtins.print') as mock_print, \
         patch('builtins.input', return_value=""):
        cli._view_cookbook_details(sample_cookbook)
    
    expected_calls = [
        call("\nCookbook: Test Cookbook"),
        call("Description: Test Description"),
        call("\nRecipes:"),
        call("- Test Recipe")
    ]
    assert mock_print.call_args_list == expected_calls

def test_delete_cookbook(cli, sample_cookbook):
    """Test deleting a cookbook."""
    cli.manager.delete_cookbook.return_value = True
    
    with patch('builtins.print'), \
         patch('builtins.input', return_value=""):
        result = cli._delete_cookbook(sample_cookbook)
    
    cli.manager.delete_cookbook.assert_called_once_with("Test Cookbook")
    assert result is True

def test_add_recipe(cli):
    """Test adding a recipe."""
    with patch('builtins.input', side_effect=["Test Recipe", "http://test.com/recipe", ""]), \
         patch('builtins.print'):
        cli._add_recipe()
    
    cli.manager.add_recipe.assert_called_once_with(
        "Test Recipe",
        "http://test.com/recipe"
    )
