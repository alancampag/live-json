from setuptools import setup


def read(filename):
    with open(filename) as f:
        return [req.strip() for req in f.readlines()]


setup(
    name="live-json",
    version="0.0.0",
    description="Write to json in real time using a dict interface",
    author="Alan Campagnaro",
    py_modules=["live_json"],
    include_package_data=True,
    extras_require={"dev": read("requirements-dev.txt")},
)
