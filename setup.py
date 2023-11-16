from setuptools import setup, find_packages

def load_readme():
    with open('README.md', 'r', encoding='utf-8') as file:
        return file.read()

setup(
    name='ntt-json-model-parser',
    version='1.1.2',
    packages=find_packages(),
    install_requires=[
    ],
    author='threezinedine',
    author_email='threezinedine@email.com',
    description='Convert data from .json file to python object',
    long_description=load_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/threezinedine/ntt-json-model-parser',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='json, parser, object',
    project_urls={
        'Source': 'https://github.com/threezinedine/ntt-json-model-parser',
        'Tracker': 'https://github.com/threezinedine/ntt-json-model-parser/issues',
    },
)