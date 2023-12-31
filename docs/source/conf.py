# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Aimiko"
copyright = "2023, Noelle"
author = "Noelle"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.napoleon", "sphinx_copybutton"]

templates_path = ["_templates"]
exclude_patterns = []

latex_elements = {
    "sphinxsetup": "verbatimwithframe=false",
}

html_title = "Aimiko"


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]


html_theme_options = {
    "dark_css_variables": {
        "color-brand-primary": "#A685E2",
        "color-brand-content": "#FFABE1",
    },
    "light_css_variables": {
        "color-brand-primary": "#6867AC",
        "color-brand-content": "#CE7BB0",
    },
}
