# -*- encoding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

setup(
    name='pyglet-pymunk-breakout-game',
    version='0.1.0',
    license='None',
    description='',
    author='Lionel ATTY',
    author_email='yoyonel@hotmail.com',
    url='',
    packages=['pyglet_pymunk.{}'.format(x) for x in find_packages('src/pyglet_pymunk')],
    package_dir={'': 'src'},
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: Pyglet',
        'Programming Language :: Python :: Implementation :: Pymunk',
        'Topic :: Utilities',
    ],
    keywords=[],
    install_requires=[
        "pyglet==1.3.2",
        "pymunk==5.3.2",    # https://stackoverflow.com/questions/45120438/pymunk-drawing-utils-not-working
                            # https://github.com/viblo/pymunk/issues/122
        # "pygame",
    ],
    entry_points={
        'console_scripts': [
            'breakout = pyglet_pymunk.breakout_game.app:main',
        ]
    },
    python_requires='>=3.5'
)
