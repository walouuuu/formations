# Automatically created by: shub deploy

from setuptools import setup, find_packages


# requirements = ['html2text'],
# requirements = ['scrapy'],
setup(
    name         = 'job_scraper',
    version      = '1.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = jobs_scraper.settings']},
    # install_requires=requirements
    install_requires=[
        'scrapy',
        'urllib3',
        'setuptools',
        'datetime',
        'html2text'
    ]
)
