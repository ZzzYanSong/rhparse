from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rhparse",
    version="0.1.0",
    author="zzzyansong",
    author_email="i@zhuyansong.com",
    description="一个用于解析原始 HTTP 数据包和格式化响应的简单 Python 库",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zzzyansong/rhparse",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "rhparse"},
    packages=find_packages(where="rhparse"),
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
    ],
)