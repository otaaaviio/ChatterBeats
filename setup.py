from setuptools import setup, find_packages

setup(
    name="otabot",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "otabot=main:main",
        ],
    },
    author="Otávio Gonçalves",
    author_email="otavio18gl@gmail.com",
    description="A discord bot that speaks messages in chat or plays music.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/otaaaviio/discord-bot",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
