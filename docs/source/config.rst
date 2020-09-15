Configuration options
=====================

The configuration options specific to ``tomyst`` which you can use in your ``conf.py`` file are:

**tomyst_static_file_path**: 

    An array which takes path of your static folders, relative to the project's ``confdir``. It creates the directory structure of the path, inside the output directory: ``_build/myst``; and then copies over the files inside the given path.

    **Example**: For config variable: ``tomyst_static_file_path: ["source/_static"]``, the contents of this folder will be copied over to ``_build/myst/source/_static``.