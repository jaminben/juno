from distutils.core import setup
import sys

try:
    import sqlalchemy
except:
    print ''
    print '** SQLAlchemy is required by Juno'
    print '** Download from: http://sqlalchemy.org/download.html'
    print '** Or run: `easy_install SQLAlchemy`'
    print ''
    sys.exit()

try:
    import flup
except:
    print ''
    print '** To use SCGI, Juno requires flup'
    print '** Download from: http://trac.saddi.com/flup/'
    print "** If you don't want SCGI, disregard this message"
    print ''

try:
    import jinja2
except:
    print ''
    print '** Jinja2 templates are the default templates for Juno'
    print '** Download from: http://pypi.python.org/pypi/Jinja2'
    print '** Or run: `easy_install Jinja2`'
    print '** Again, Jinja2 is not required.'
    print ''

setup(name         = 'juno',
      description  = 'A lightweight Python web framework',
      author       = 'Brian Reily',
      author_email = 'brian@brianreily.com',
      url          = 'http://brianreily.com/project/juno/',
      version      = '0.1',
      py_modules   = ['juno'],
     )
