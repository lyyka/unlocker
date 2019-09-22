import setuptools

setuptools.setup(
    name='unlocker',
    version='1.1',
    author='Luka Robajac',
    author_email='luka.robajac@gmail.com',
    description='Breaks all locks on a file',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'unlocker = unlocker.unlocker:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)