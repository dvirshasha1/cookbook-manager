from typing import List, Optional, Tuple, Any
from pick import pick
from .models import Recipe, Cookbook
from .app import CookbookManager

class CookbookCLI:
    """! @brief Command Line Interface for the Cookbook Manager application.
    
    This class provides an interactive CLI using the pick package for managing cookbooks and recipes.
    It delegates all business logic to the CookbookManager class.
    """
    
    def __init__(self):
        """Initialize the CLI with a CookbookManager instance."""
        self.manager = CookbookManager()
        
    def main_menu(self) -> None:
        """Display the main menu and handle user selection."""
        while True:
            title = 'Cookbook Manager - Main Menu'
            options = [
                'Manage Cookbooks',
                'Manage Recipes',
                'Exit'
            ]
            
            option, _ = pick(options, title)
            if option == 'Manage Cookbooks':
                self.cookbook_menu()
            elif option == 'Manage Recipes':
                self.recipe_menu()
            else:
                break
    
    def cookbook_menu(self) -> None:
        """Display the cookbook management menu."""
        while True:
            title = 'Cookbook Management'
            options = [
                'View All Cookbooks',
                'Add New Cookbook',
                'Select Cookbook to Manage',
                'Back to Main Menu'
            ]
            
            option, _ = pick(options, title)
            if option == 'View All Cookbooks':
                self._view_all_cookbooks()
            elif option == 'Add New Cookbook':
                self._add_cookbook()
            elif option == 'Select Cookbook to Manage':
                self._manage_cookbook()
            else:
                break
    
    def _get_input(self, prompt: str) -> str:
        """Get user input with a prompt."""
        return input(prompt)
    
    def _view_all_cookbooks(self) -> None:
        """Display all cookbooks."""
        cookbooks = self.manager.get_all_cookbooks()
        if not cookbooks:
            print("\nNo cookbooks found.")
        else:
            print("\nAvailable Cookbooks:")
            for cookbook in cookbooks:
                print(f"- {cookbook.name}")
        input("\nPress Enter to continue...")
    
    def _add_cookbook(self) -> None:
        """Add a new cookbook."""
        name = self._get_input("\nEnter cookbook name: ")
        description = self._get_input("Enter description (optional): ")
        
        cookbook = self.manager.add_cookbook(name, description if description else None)
        print("\nCookbook added successfully!")
        input("\nPress Enter to continue...")
    
    def _select_cookbook(self) -> Optional[Cookbook]:
        """Let user select a cookbook from the list."""
        cookbooks = self.manager.get_all_cookbooks()
        if not cookbooks:
            print("\nNo cookbooks found.")
            input("\nPress Enter to continue...")
            return None
            
        title = 'Select a Cookbook'
        options = [c.name for c in cookbooks]
        option, index = pick(options, title)
        return cookbooks[index]
    
    def _manage_cookbook(self) -> None:
        """Display management options for a selected cookbook."""
        cookbook = self._select_cookbook()
        if not cookbook:
            return
            
        while True:
            title = f'Managing Cookbook: {cookbook.name}'
            options = [
                'View Cookbook Details',
                'Add Recipe to Cookbook',
                'Remove Recipe from Cookbook',
                'Delete Cookbook',
                'Back to Cookbook Menu'
            ]
            
            option, _ = pick(options, title)
            if option == 'View Cookbook Details':
                self._view_cookbook_details(cookbook)
            elif option == 'Add Recipe to Cookbook':
                self._add_recipe_to_cookbook(cookbook)
            elif option == 'Remove Recipe from Cookbook':
                self._remove_recipe_from_cookbook(cookbook)
            elif option == 'Delete Cookbook':
                if self._delete_cookbook(cookbook):
                    break
            else:
                break
    
    def _view_cookbook_details(self, cookbook: Cookbook) -> None:
        """Display details of a cookbook."""
        print(f"\nCookbook: {cookbook.name}")
        print(f"Description: {cookbook.description}")
        print("\nRecipes:")
        for recipe in cookbook.recipes:
            print(f"- {recipe.name}")
        input("\nPress Enter to continue...")
    
    def _delete_cookbook(self, cookbook: Cookbook) -> bool:
        """Delete a cookbook."""
        if self.manager.delete_cookbook(cookbook.name):
            print("\nCookbook deleted successfully!")
            input("\nPress Enter to continue...")
            return True
        print("\nFailed to delete cookbook.")
        input("\nPress Enter to continue...")
        return False
    
    def recipe_menu(self) -> None:
        """Display the recipe management menu."""
        while True:
            title = 'Recipe Management'
            options = [
                'View All Recipes',
                'Add New Recipe',
                'View Recipe Details',
                'Delete Recipe',
                'Back to Main Menu'
            ]
            
            option, _ = pick(options, title)
            if option == 'View All Recipes':
                self._view_all_recipes()
            elif option == 'Add New Recipe':
                self._add_recipe()
            elif option == 'View Recipe Details':
                self._view_recipe_details()
            elif option == 'Delete Recipe':
                self._delete_recipe()
            else:
                break
    
    def _view_all_recipes(self) -> None:
        """Display all recipes."""
        recipes = self.manager.get_all_recipes()
        if not recipes:
            print("\nNo recipes found.")
        else:
            print("\nAvailable Recipes:")
            for recipe in recipes:
                print(f"- {recipe.name}")
        input("\nPress Enter to continue...")
    
    def _add_recipe(self) -> None:
        """Add a new recipe."""
        name = self._get_input("\nEnter recipe name: ")
        url = self._get_input("Enter recipe URL: ")
        
        recipe = self.manager.add_recipe(name, url)
        print("\nRecipe added successfully!")
        input("\nPress Enter to continue...")
    
    def _select_recipe(self) -> Optional[Recipe]:
        """Let user select a recipe from the list."""
        recipes = self.manager.get_all_recipes()
        if not recipes:
            print("\nNo recipes found.")
            input("\nPress Enter to continue...")
            return None
            
        title = 'Select a Recipe'
        options = [r.name for r in recipes]
        option, index = pick(options, title)
        return recipes[index]
    
    def _view_recipe_details(self) -> None:
        """Display details of a selected recipe."""
        recipe = self._select_recipe()
        if recipe:
            print(f"\nRecipe: {recipe.name}")
            print(f"URL: {recipe.url}")
            input("\nPress Enter to continue...")
