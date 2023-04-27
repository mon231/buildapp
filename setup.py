import setuptools


setuptools.setup(
    name = "buildapp",
    version = "1.1.1",
    author = "Ariel Tubul",
    description = "Apk builder script",
    packages = setuptools.find_packages(),
    url = "https://github.com/mon231/buildapp/",
    entry_points = {'console_scripts': ['buildapp=buildapp.buildapp:main']}
)
