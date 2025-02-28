from setuptools import setup, find_packages

setup(
    name="ChatterBeats",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "discord.py",
        "python-dotenv",
        "gtts",
    ],
    entry_points={
        "console_scripts": [
            "ChatterBeats=main:main",
        ],
    },
    author="Otávio Gonçalves",
    author_email="otavio18gl@gmail.com",
    description="A discord bot that speaks messages in chat.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/otaaaviio/ChatterBeats",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
