from setuptools import setup, find_packages


setup(
    name="bumblebee-tools",
    version="0.1.0",
    packages=find_packages(),

    install_requires=[
        'PyGObject>=3.34.0',
        'pynput==1.6.8'
    ],

    entry_points={
        #"console_scripts": [
        #    "foo = my_package.some_module:main_func",
        #    "bar = other_module:some_func",
        #],
        "gui_scripts": [
            "bumblebee_tools = bumblebee_tools.main:init",
        ]
    },

    include_package_data=True,
 
    #package_data={
    #    # If any package contains *.txt or *.rst files, include them:
    #    "": ["*.txt", "*.rst"],
    #    # And include any *.msg files found in the "hello" package, too:
    #    "hello": ["*.msg"],
    #},

    # metadata to display on PyPI
    author="Jonhnatha Trigueiro",
    author_email="joepreludian@gmail.com",
    description="This is a very simple tool with some tools",

    keywords="bumblebee intelvirtualoutput",
    url="https://github.com/joepreludian/bumblebee_tools",   # project home page, if any
    project_urls={
        "Bug Tracker": "https://github.com/joepreludian/bumblebee_tools/issues/new",
        "Documentation": "https://github.com/joepreludian/bumblebee_tools",
        "Source Code": "https://github.com/joepreludian/bumblebee_tools",
    },

    classifiers=[
        "License :: OSI Approved :: Python Software Foundation License"
    ]

    # could also include long_description, download_url, etc.
)
