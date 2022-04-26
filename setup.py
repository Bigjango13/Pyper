from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="pyper-piper",
    version="0.1.6",
    description="The Piper networking protocol in Python.",
    url="https://github.com/Bigjango13/Pyper",
    author="Bigjango13",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["pyper"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Communications",
        "Topic :: Communications :: File Sharing",
        "Topic :: Internet",
        "Topic :: System :: Networking",
    ],
)
