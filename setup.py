import setuptools
import re

long_description = ''
with open("README.md", "r") as fh:
    long_description = fh.read()

version = ''
with open('rebootpy/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

requirements = ['aiohttp>=3.12.7', 'aioxmpp>=0.13.3', 'aioconsole>=0.1.15', 'pytz>=2024.2']
try:
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
except FileNotFoundError:
    pass

extras_require = {
    'docs': [
        'sphinxcontrib_trio==1.1.2',
        'furo==2021.4.11b34',
        'Jinja2<3.1',
    ]
}

setuptools.setup(
    name="rebootpy",
    url="https://github.com/xMistt/rebootpy",
    project_urls={
        "Documentation": "https://rebootpy.readthedocs.io/en/latest/",
        "Issue tracker": "https://github.com/xMistt/rebootpy/issues",
    },
    version=version,
    author="xMistt",
    description="Library for interacting with fortnite services",
    long_description=long_description,
    license='MIT',
    long_description_content_type="text/markdown",
    install_requires=requirements,
    extras_require=extras_require,
    packages=['rebootpy', 'rebootpy.ext.commands'],
    python_requires='>=3.7.0',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
