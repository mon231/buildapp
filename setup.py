import setuptools
from pathlib import Path


CURRENT_FOLDER = Path(__file__).parent
README_PATH = CURRENT_FOLDER / 'README.md'


setuptools.setup(
    name = "buildapp",
    version = "1.1.3",
    author = "Ariel Tubul",
    description = "Apk builder script",
    packages = setuptools.find_packages(),
    long_description = README_PATH.read_text(),
    url = "https://github.com/mon231/buildapp/",
    long_description_content_type='text/markdown',
    entry_points = {'console_scripts': ['buildapp=buildapp.buildapp:main']}
)
