from typing import List

from setuptools import find_packages, setup

hypen_e_dot = "-e ."


def get_requirements(file_path: str) -> List:
    """
    return all of the packages required
    """
    with open(file_path) as f:
        requirements = f.readlines()
        requirements = [req.replace("\n", "") for req in requirements]
        if hypen_e_dot in requirements:
            requirements.remove(hypen_e_dot)
    return requirements


setup(
    name="ML_Projects",
    version="0.01",
    author="Zhi Li",
    author_email="zhl026@ucsd.edu",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
)
