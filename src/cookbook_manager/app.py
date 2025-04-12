"""! @brief Application logic for cookbook management.

This module contains the core business logic for managing cookbooks and recipes,
separate from the user interface.
"""

from typing import List, Optional, Dict
from .models import Recipe, Cookbook
from .database import JsonDatabase

class CookbookManager:
    """! @brief Core application logic for managing cookbooks and recipes.
    
    This class handles all the business logic for managing cookbooks and recipes,
    independent of any user interface.
    """
    
    def __init__(self):
        """Initialize the cookbook manager with database connections."""
        self.cookbook_db = JsonDatabase[Cookbook]('cookbooks.json')
        self.recipe_db = JsonDatabase[Recipe]('recipes.json')
    
    def add_cookbook(self, name: str, description: Optional[str] = None) -> Cookbook:
        """! Add a new cookbook to the database.
        @param name The name of the cookbook
        @param description An optional description of the cookbook
        @return The newly created cookbook
        """
        cookbook = Cookbook(name=name, description=description)
        self.cookbook_db.insert(cookbook)
        return cookbook
    
    def get_all_cookbooks(self) -> List[Cookbook]:
        """! Get all cookbooks from the database.
        @return List of all cookbooks
        """
        cookbooks_data = self.cookbook_db.get_all()
        return [Cookbook(**data) for data in cookbooks_data]
    
    def get_cookbook_by_name(self, name: str) -> Optional[Cookbook]:
        """! Get a cookbook by its name.
        @param name The name of the cookbook to find
        @return The cookbook if found, None otherwise
        """
        data = self.cookbook_db.find_by_field('name', name)
        return Cookbook(**data) if data else None
    
    def delete_cookbook(self, name: str) -> bool:
        """! Delete a cookbook by its name.
        @param name The name of the cookbook to delete
        @return True if deleted successfully, False otherwise
        """
        return self.cookbook_db.delete_by_field('name', name)
    
    def add_recipe(self, name: str, url: str) -> Recipe:
        """! Add a new recipe to the database.
        @param name The name of the recipe
        @param url The URL where the recipe can be found
        @return The newly created recipe
        """
        recipe = Recipe(name=name, url=url)
        self.recipe_db.insert(recipe)
        return recipe
    
    def get_all_recipes(self) -> List[Recipe]:
        """! Get all recipes from the database.
        @return List of all recipes
        """
        recipes_data = self.recipe_db.get_all()
        return [Recipe(**data) for data in recipes_data]
    
    def get_recipe_by_name(self, name: str) -> Optional[Recipe]:
        """! Get a recipe by its name.
        @param name The name of the recipe to find
        @return The recipe if found, None otherwise
        """
        data = self.recipe_db.find_by_field('name', name)
        return Recipe(**data) if data else None
    
    def delete_recipe(self, name: str) -> bool:
        """! Delete a recipe by its name.
        @param name The name of the recipe to delete
        @return True if deleted successfully, False otherwise
        """
        return self.recipe_db.delete_by_field('name', name)
    
    def add_recipe_to_cookbook(self, cookbook_name: str, recipe_name: str) -> bool:
        """! Add a recipe to a cookbook.
        @param cookbook_name The name of the cookbook
        @param recipe_name The name of the recipe to add
        @return True if added successfully, False otherwise
        """
        cookbook_data = self.cookbook_db.find_by_field('name', cookbook_name)
        recipe_data = self.recipe_db.find_by_field('name', recipe_name)
        
        if not cookbook_data or not recipe_data:
            return False
            
        cookbook = Cookbook(**cookbook_data)
        recipe = Recipe(**recipe_data)
        
        # Check if recipe already exists in cookbook
        if any(r.name == recipe.name for r in cookbook.recipes):
            return False
            
        cookbook.recipes.append(recipe)
        return self.cookbook_db.update_by_field('name', cookbook_name, cookbook.model_dump())
