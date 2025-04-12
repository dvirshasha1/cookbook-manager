from typing import List, Optional, Tuple, Any
from pick import pick
from .models import Recipe, Cookbook
from .database import JsonDatabase

class CookbookCLI:
    """! @brief Command Line Interface for the Cookbook Manager application.
    
    This class provides an interactive CLI using the pick package for managing cookbooks and recipes.
    """
    
    def __init__(self):
        self.cookbook_db = JsonDatabase[Cookbook]('cookbooks.json')
        self.recipe_db = JsonDatabase[Recipe]('recipes.json')
        
    def main_menu(self) -> None:
        """Display the main menu and handle user selection."""
        title = 'Cookbook Manager - Main Menu'
        options = [
            'Manage Cookbooks',
            'Manage Recipes',
            'Exit'
        ]
        
        while True:
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
    
    def recipe_menu(self) -> None:
        """Display the recipe management menu."""
        title = 'Recipe Management'
        options = [
            'View All Recipes',
            'Add New Recipe',
            'View Recipe Details',
            'Delete Recipe',
            'Back to Main Menu'
        ]
        
        while True:
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

    def _get_input(self, prompt: str) -> str:
        """Get input from user with proper terminal handling."""
        print(prompt)
        return input().strip()
    
    def _select_cookbook(self) -> Optional[Cookbook]:
        """Helper method to select a cookbook from the list."""
        cookbooks = self.cookbook_db.get_all()
        if not cookbooks:
            print("\nNo cookbooks available.")
            return None
            
        options = [f"{cb['name']}" for cb in cookbooks]
        options.append("Cancel")
        title = "Select a Cookbook"
        selected, _ = pick(options, title)
        
        if selected == "Cancel":
            return None
            
        return next((Cookbook(**cb) for cb in cookbooks if cb['name'] == selected), None)
    
    def _select_recipe(self) -> Optional[Recipe]:
        """Helper method to select a recipe from the list."""
        recipes = self.recipe_db.get_all()
        if not recipes:
            print("\nNo recipes available.")
            return None
            
        options = [f"{r['name']}" for r in recipes]
        options.append("Cancel")
        title = "Select a Recipe"
        selected, _ = pick(options, title)
        
        if selected == "Cancel":
            return None
            
        return next((Recipe(**r) for r in recipes if r['name'] == selected), None)
    
    # Placeholder methods for actual implementations
    def _view_all_cookbooks(self) -> None:
        cookbooks = self.cookbook_db.get_all()
        if not cookbooks:
            print("\nNo cookbooks available.")
            return
        print("\nAvailable Cookbooks:")
        for cb in cookbooks:
            print(f"- {cb['name']}")
        input("\nPress Enter to continue...")
    
    def _add_cookbook(self) -> None:
        name = self._get_input("\nEnter cookbook name: ")
        description = self._get_input("Enter description (optional): ")
        cookbook = Cookbook(name=name, description=description if description else None)
        self.cookbook_db.insert(cookbook)
        print("\nCookbook added successfully!")
        input("\nPress Enter to continue...")
    
    def _view_cookbook_details(self, cookbook: Cookbook) -> None:
        print(f"\nCookbook: {cookbook.name}")
        print(f"Description: {cookbook.description or 'No description'}")
        print("\nRecipes:")
        for recipe in cookbook.recipes:
            print(f"- {recipe.name}")
        input("\nPress Enter to continue...")
    
    def _add_recipe_to_cookbook(self, cookbook: Cookbook) -> None:
        recipe = self._select_recipe()
        if not recipe:
            return
            
        cookbook_data = self.cookbook_db.find_by_field('name', cookbook.name)
        if cookbook_data:
            cookbook_data['recipes'].append(recipe.model_dump())
            self.cookbook_db.update_by_field('name', cookbook.name, cookbook_data)
            print("\nRecipe added to cookbook successfully!")
        input("\nPress Enter to continue...")
    
    def _remove_recipe_from_cookbook(self, cookbook: Cookbook) -> None:
        if not cookbook.recipes:
            print("\nNo recipes in this cookbook.")
            input("\nPress Enter to continue...")
            return
            
        options = [f"{recipe.name}" for recipe in cookbook.recipes]
        options.append("Cancel")
        title = "Select Recipe to Remove"
        selected, _ = pick(options, title)
        
        if selected != "Cancel":
            cookbook_data = self.cookbook_db.find_by_field('name', cookbook.name)
            cookbook_data['recipes'] = [r for r in cookbook_data['recipes'] 
                                      if r['name'] != selected]
            self.cookbook_db.update_by_field('name', cookbook.name, cookbook_data)
            print("\nRecipe removed from cookbook successfully!")
        input("\nPress Enter to continue...")
    
    def _delete_cookbook(self, cookbook: Cookbook) -> bool:
        if self.cookbook_db.delete_by_field('name', cookbook.name):
            print("\nCookbook deleted successfully!")
            return True
        else:
            print("\nFailed to delete cookbook.")
            input("\nPress Enter to continue...")
            return False
    
    def _view_all_recipes(self) -> None:
        recipes = self.recipe_db.get_all()
        if not recipes:
            print("\nNo recipes available.")
            return
        print("\nAvailable Recipes:")
        for recipe in recipes:
            print(f"- {recipe['name']}: {recipe['url']}")
        input("\nPress Enter to continue...")
    
    def _add_recipe(self) -> None:
        name = self._get_input("\nEnter recipe name: ")
        url = self._get_input("Enter recipe URL: ")
        recipe = Recipe(name=name, url=url)
        self.recipe_db.insert(recipe)
        print("\nRecipe added successfully!")
        input("\nPress Enter to continue...")
    
    def _view_recipe_details(self) -> None:
        recipe = self._select_recipe()
        if recipe:
            print(f"\nRecipe: {recipe.name}")
            print(f"URL: {recipe.url}")
            input("\nPress Enter to continue...")
    
    def _delete_recipe(self) -> None:
        recipe = self._select_recipe()
        if recipe:
            if self.recipe_db.delete_by_field('name', recipe.name):
                print("\nRecipe deleted successfully!")
            else:
                print("\nFailed to delete recipe.")
        input("\nPress Enter to continue...")
