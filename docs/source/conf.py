import os
import sys

import sphinx_rtd_theme

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
sys.path.insert(0, os.path.abspath('../..'))

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'nbsphinx',
]

napoleon_use_ivar = True

googleanalytics_id = 'UA-90545585-1'
googleanalytics_enabled = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = ['.rst', '.ipynb']

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'PyTorch Geometry'
copyright = u'2018, Arraiy, Inc.'
author = u'Arraiy, Inc.'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.

#version = 'master (' + torchgeometry.__version__ + ' )'
version = ''

if 'READTHEDOCS' not in os.environ:
    # if developing locally, use pyro.__version__ as version
    from torchgeometry import __version__  # noqaE402
    version = __version__

#release = 'master'
release = version

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['.ipynb_checkpoints']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# do not prepend module name to functions
add_module_names = False

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    'collapse_navigation': False,
    'display_version': True,
    'logo_only': True,
}

html_logo = '_static/img/torchgeometry_logo.svg'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# html_style_path = 'css/pytorch_theme.css'
html_context = {
    'css_files': [
        'https://fonts.googleapis.com/css?family=Lato',
        '_static/css/pytorch_theme.css'
    ],
}

# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'PyTorchGeometry'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'PytorchGeometry.tex', u'PyTorch Geometry Documentation',
     u'Arraiy', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'PyTorch Geometry', 'PyTorch Geometry Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'torchgeometry', 'torchgeometry Documentation',
     author, 'torchgeometry', 'One line description of project.',
     'Miscellaneous'),
]


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'numpy': ('http://docs.scipy.org/doc/numpy/', None),
    'torch': ('http://pytorch.org/docs/master/', None),
}

# -- A patch that prevents Sphinx from cross-referencing ivar tags -------
# See http://stackoverflow.com/a/41184353/3343043

from docutils import nodes
from sphinx.util.docfields import TypedField
from sphinx import addnodes


def patched_make_field(self, types, domain, items, **kw):
    # `kw` catches `env=None` needed for newer sphinx while maintaining
    #  backwards compatibility when passed along further down!

    # type: (List, unicode, Tuple) -> nodes.field
    def handle_item(fieldarg, content):
        par = nodes.paragraph()
        par += addnodes.literal_strong('', fieldarg)  # Patch: this line added
        # par.extend(self.make_xrefs(self.rolename, domain, fieldarg,
        #                           addnodes.literal_strong))
        if fieldarg in types:
            par += nodes.Text(' (')
            # NOTE: using .pop() here to prevent a single type node to be
            # inserted twice into the doctree, which leads to
            # inconsistencies later when references are resolved
            fieldtype = types.pop(fieldarg)
            if len(fieldtype) == 1 and isinstance(fieldtype[0], nodes.Text):
                typename = u''.join(n.astext() for n in fieldtype)
                typename = typename.replace('int', 'python:int')
                typename = typename.replace('long', 'python:long')
                typename = typename.replace('float', 'python:float')
                typename = typename.replace('type', 'python:type')
                par.extend(self.make_xrefs(self.typerolename, domain, typename,
                                           addnodes.literal_emphasis, **kw))
            else:
                par += fieldtype
            par += nodes.Text(')')
        par += nodes.Text(' -- ')
        par += content
        return par

    fieldname = nodes.field_name('', self.label)
    if len(items) == 1 and self.can_collapse:
        fieldarg, content = items[0]
        bodynode = handle_item(fieldarg, content)
    else:
        bodynode = self.list_type()
        for fieldarg, content in items:
            bodynode += nodes.list_item('', handle_item(fieldarg, content))
    fieldbody = nodes.field_body('', bodynode)
    return nodes.field('', fieldname, fieldbody)


TypedField.make_field = patched_make_field

# @jpchen's hack to get rtd builder to install latest pytorch
if 'READTHEDOCS' in os.environ:
    os.system("pip install pytorch-cpu==1.0.0")
#    os.system('pip install http://download.pytorch.org/whl/cpu/torch-0.4.1-cp27-cp27mu-linux_x86_64.whl')
    # for pytorch 1.0 (currently fails with OOM
    # https://readthedocs.org/projects/pyro-ppl/builds/8159615/
    #     os.system('pip install torch_nightly==1.0.0.dev20181127 -f '
    #               'https://download.pytorch.org/whl/nightly/cpu/torch_nightly.html')
