#!/usr/bin/env python
"""Main entry point for the Cookbook Manager CLI application."""
from cookbook_manager.cli import CookbookCLI

def main():
    cli = CookbookCLI()
    cli.main_menu()

if __name__ == "__main__":
    main()
