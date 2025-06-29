from setuptools import setup, find_packages

setup(
    name="customrag",
    version="0.1.1",
    author="Anuj Goel",
    description="A customizable RAG pipeline supporting multiple LLM providers and embedding backends.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",  # 🧠 important for proper rendering
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        line.strip() for line in open("requirements.txt") if line.strip() and not line.startswith("#")
    ],
    entry_points={
        "console_scripts": [
            "customrag-setup=customrag_setup:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
