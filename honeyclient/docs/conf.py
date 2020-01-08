project = "TR-069 Honeyclient"
master_doc = "index"

extensions = [
    'sphinx.ext.autodoc',
    'sphinxcontrib.napoleon',
#    'sphinx_autodoc_typehints',
    'sphinx.ext.intersphinx',
]
autoclass_content = 'both'

intersphinx_mapping = {
	'requests': ('http://docs.python-requests.org/en/stable/', None),
    'python': ('https://docs.python.org/3', None),
}

autodoc_member_order = 'bysource'
autodoc_default_flags = ["members"]

html_theme = "alabaster"
html_theme_options = {
#    'show_powered_by': False,
#'logo_only': True,
#'navigation_depth': 0,
}
html_show_copyright = False
html_show_sourcelink = False
html_sidebars = {
    '**': []
}
