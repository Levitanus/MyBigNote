import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MyBigNote-LEVITANUS",  # Replace with your own username
    version="0.0.1",
    author="Levitanus",
    author_email="pianoist@ya.ru",
    description="Small gui app for displaying one big note.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Levitanus/MyBigNote",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GNU/GPLv3",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['my_big_note = my_big_note.__main__:main']
    },
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
)
