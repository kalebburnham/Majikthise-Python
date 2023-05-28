from distutils.core import setup
from Cython.Build import cythonize

#python3 setup.py build_ext --inplace
#cythonize -i bitboard.pyx   


setup(ext_modules=cythonize(['bitboard.pyx', 'board.pyx', 'movegen.pyx', 'rays.pyx'], compiler_directives={'language_level' : "3"}))