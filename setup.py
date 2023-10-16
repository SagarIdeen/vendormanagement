from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in vendormanagement/__init__.py
from vendormanagement import __version__ as version

setup(
	name="vendormanagement",
	version=version,
	description="Vendor Management",
	author="Ideenkreice",
	author_email="vendor@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
