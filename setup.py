from setuptools import setup, find_packages

setup(
    name="vocab_reminder_google_cert",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
