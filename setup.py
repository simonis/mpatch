from distutils.core import setup, Extension
import mpatch.version
setup(name='mpatch',
      version=mpatch.version.version,
      ext_modules=[Extension('mpatch.diffhelpers', ['mpatch/diffhelpers.c']),
                   Extension('mpatch.base85', ['mpatch/base85.c'])],
      scripts=['cmd/mpatch'],
      packages=['mpatch'])
