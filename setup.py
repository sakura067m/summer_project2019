from setuptools import setup

requirements = [
    "PyQt5>=5.13.1",
    "numpy",
    "matplotlib>=3.1.0",
    "Pillow>=6.1.0",
    "selenium==3.141.0",
    "requests==2.22.0",
    "lxml==4.6.2",
    "urllib3==1.25.3"
]


setup(
    name="QSP2019",
    version="0.9.0",
    description="Programs used in Summer Project 2019.",
    url="https://github.com/sakura067m/summer_project2019",
    author="sakura067m",
    author_email="3IE19001M@s.kyushu-u.ac.jp",
##    license='',  # TBD
    packages=["iAnnotator", "cAnnotator"],
    package_dir={"iAnnotator": "iAnnotator",
                 "cAnnotator": "cAnnotator",
                 },
    package_data={
        "iAnnotator":["labels.txt"],
        "cAnnotator":["labels.txt"],
    },
    scripts=["getimg3.py"],
    entry_points={
        "gui_scripts": ["iAnnotator = iAnnotator.__main__:main",
                        "cAnnotator = cAnnotator.__main__:main"]
    },
    install_requires=requirements,
    python_requires='>=3.4',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
    ],
)
