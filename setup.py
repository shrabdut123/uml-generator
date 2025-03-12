from setuptools import setup, find_packages

setup(
    name="uml-generator",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "openai",
        "networkx",
        "matplotlib",
        "PyExecJS",  # Correct package name
        "azure-identity"
    ],
    entry_points={
        'console_scripts': [
            'uml-generator=uml_generator_cli:main',  # entry point to the main function
        ],
    },
)