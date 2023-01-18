from setuptools import setup, find_packages

setup(
    name='twitter_sentiment_api',
    version='1.0.0',
    description='Flask-based api for twitter sentiment analysis',
    license='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)

