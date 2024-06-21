from setuptools import setup, find_packages

setup(
    name="chessvision",
    version="0.0.1",
    author="Benedict Wilkins",
    author_email="benrjw@gmail.com",
    description="",
    long_description=open("../README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/BenedictWilkins/chess-vision",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
    ],
    install_requires=[
        "ultralytics",
        "pillow",
        "tqdm",
        "pynput",
        "matplotlib",
    ],
    python_requires=">=3.10",
)
