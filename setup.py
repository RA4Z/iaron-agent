from cx_Freeze import setup, Executable

import sys

sys.setrecursionlimit(10**6)

build_exe_options = {
    "packages": ["flet", "docx", "progressbar", "requests", "openpyxl", "google.generativeai", "win32com", "PyPDF2"],
    "excludes": ["unittest", "tkinter", "navigator-updater", "nbclassic", "nbclient", "nbconvert", "nbformat",
                 "networkx", "nltk", "nose", "notebook", "numba", "numexpr", "numpy", "numpy-base", "numpydoc",
                 "pandas", "pandocfilters", "panel", "param", "paramiko", "parsel", "parso", "partd",
                 "pathspec", "patsy", "pep8", "pexpect", "pickleshare", "pillow", "pkginfo", "plotly", "pluggy",
                 "powershell_shortcut", "poyo", "prometheus_client", "prompt-toolkit", "protego", "protobuf",
                 "pure_eval", "flask"],
    "include_files": ["assets/", "database/", "languages/", "Systems/"]
}

target = Executable(
    script="main.py",
    target_name="IAron Agent AI",
    base="Win32GUI",
    copyright="Robert Aron Zimmermann",
    icon="assets/IAron.ico"
)

setup(
    name="IAron Agent AI",
    version="0.1",
    description="IAron Agent - Developed by Robert Aron Zimmermann robertn@weg.net",
    options={"build_exe": build_exe_options},
    executables=[target],
)

# python setup.py build --force
