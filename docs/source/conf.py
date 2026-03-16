# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Switchbot Utility Document'
copyright = '2026, MATSUMURA Hidetoshi'
author = 'MATSUMURA Hidetoshi'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',   # ソースコード読み込み用
    'sphinx.ext.napoleon',  # docstring パース用
    'sphinx_rtd_theme',     # Read the Docs テーマ (今回は不要*1)
    'sphinx_multiversion',  # マルチバージョン用
]

templates_path = ['_templates']
exclude_patterns = []

language = 'ja'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Options for sphinx-multiversion -----------------------------------------

smv_tag_whitelist = r'^\d+\.\d+$'   # これにマッチしたタグを抽出
smv_branch_whitelist = r'^main$'  # これにマッチしたブランチを抽出
