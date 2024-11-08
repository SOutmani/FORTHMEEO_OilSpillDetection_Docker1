"""oilspill001"""
import os
import setuptools
VERSION = "0.1.0"
BASEDIR = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
with open(os.path.join(BASEDIR, "README.md"), "r") as f:
    readme = f.read()

#    packages=setuptools.find_packages(where="src"),
    #package_dir={"":"src"},

setuptools.setup(
    name="oilspill001",
    version=VERSION,
    author="MEEO S.r.l.",
    author_email="info@meeo.it",
    description="Iliad - Oil spill detection - Application Package 1",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://meeo.it",
    license="Apache 2.0",
    packages=setuptools.find_packages(where="src"),
    package_dir={"":"src"},
    install_requires=[
        "asf-search", 
        "click",
        "python-dotenv",
        "shapely"
    ],
    extras_require={
        "dev": [
            "pre-commit",
            "tox",
            "pytest",
        ]
    },
    entry_points={
        "console_scripts": [
            "oilspill001 = oilspill001.main:main",
        ]
    },
    project_urls={
        "Bug Tracker": "https://github.com/SOutmani/FORTHMEEO_OilSpillDetection_Docker1/issues",
        "Documentation": "https://github.com/SOutmani/FORTHMEEO_OilSpillDetection_Docker1/ILIAD_OilSpills",
        "Source Code": "https://github.com/SOutmani/FORTHMEEO_OilSpillDetection_Docker1/ILIAD_OilSpills",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    package_data={},
    include_package_data=True,
)
