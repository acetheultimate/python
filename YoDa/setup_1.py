from distutils.core import setup
import py2exe
import sys

if len(sys.argv) == 1:
    sys.argv.append("py2exe")
    sys.argv.append("-i")
    sys.argv.append("dbhash")
    

class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        self.version = "1.9.9"
        self.company_name = "FeedAbyte"
        self.author = "Yogi"
        self.author_email='acetheultimate@gmail.com'
        self.copyright = "Copyright (c) 2016 FeedAbyte"
        self.name = "YoDa"
        self.publisher = 'FeedAbyte'

target = Target(
    description = "Paste the link and download the media",
    script = "YoDa.py",
    icon_resources = [(0,"icon.ico")]
    )

setup(
    options = {'py2exe': {'compressed': True}},
    zipfile = None,
    windows = [target]
)
