from pydantic import BaseModel
from typing import List, Optional

class Recipe(BaseModel):
    """! @brief A class representing a recipe with a name and URL.
    
    This class stores basic information about a recipe, including its name and the URL where it can be found.
    """
    
    name: str  #!< The name of the recipe
    url: str   #!< The URL where the recipe can be found

class Cookbook(BaseModel):
    """! @brief A class representing a cookbook containing multiple recipes.
    
    This class represents a cookbook that can contain multiple recipes. Each cookbook has a name,
    an optional description, and a list of recipes.
    """
    
    name: str  #!< The name of the cookbook
    description: Optional[str] = None  #!< An optional description of the cookbook
    recipes: List[Recipe] = []  #!< A list of recipes contained in the cookbook
