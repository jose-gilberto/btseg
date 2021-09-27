import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()


setuptools.setup(
    name="btseg",
    version="0.0.1",
    author="Gilberto Medeiros",
    author_email="medeiros.gilberto.br@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jose-gilberto/btseg",
    project_urls={
        "Bug Tracker": "https://github.com/jose-gilberto/btseg/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "btseg"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)