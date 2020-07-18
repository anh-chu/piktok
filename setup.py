import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="piktok",
    version="0.0.1",
    author="Anh Chu",
    author_email="chuducanh.atred@gmail.com",
    description="A module to retrieve data from TikTok",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anh-chu/piktok",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
