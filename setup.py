import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="approvals_validator",
    version="0.2.1",
    author="Jake Romer",
    author_email="mail@jakeromer.com",
    description="A CLI tool to validate changeset approvals.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jmromer/approvals_validator",
    install_requires=["click", "colorama"],
    packages=setuptools.find_packages(),
    scripts=["validate_approvals"],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
