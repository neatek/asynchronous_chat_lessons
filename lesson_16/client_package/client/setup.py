from setuptools import setup, find_packages
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": [
        "os",
        "sqlalchemy",
        "PyQt5",
        # "pycryptodome",
        # "pycryptodomex",
    ],
    "excludes": ["tkinter"],
}

setup(
    name="neatek-python-chat-client",
    version="0.1",
    description="Client packet",
    packages=find_packages(),
    author_email="neatek@icloud.com",
    author="Vladimir Zhelnov",
    options={"build_exe": build_exe_options},
    executables=[Executable("client.py")],
)