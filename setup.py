from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["flet", "docx", "progressbar", "requests",
                 "openpyxl", "google.generativeai",
                 "win32com", "PyPDF2"],

    "includes": ["atexit"],
    "excludes": ["unittest"],
    "include_files": ["assets/", "database/", "languages/", "artificial_intelligence/", "Systems/"]
}

target = Executable(
    script="main.py",
    base="Win32GUI",
    icon="assets/IAron.ico"
)

setup(
    name="iaron-agent",
    version="0.1",
    description="IAron PPC Agent",
    options={"build_exe": build_exe_options},
    executables=[target],
)

# python setup.py build
