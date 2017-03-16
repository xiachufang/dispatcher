from distutils.core import setup

setup(
    name='pypydispatch',
    maintainer='gfreezy',
    maintainer_email='gfreezy@gmail.com',
    description='A library for event-driven programming, extracted from Django',
    packages=[
        'dispatcher',
    ],
    version='1.0.5',
    url='https://github.com/xiachufang/dispatcher',
    install_requires=[
        'celery',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
