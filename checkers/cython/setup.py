from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize(r"D:\Users\Juweriah\Documents\python\tictactoe\checkers\cython\checgame.pyx")
)
'''setup(
ext_modules=cythonize([
    "game_logic.pyx",
    "gui.pyx",
    "main.pyx"
]),
zip_safe=False
)
'''

#python D:\Users\Juweriah\Documents\python\tictactoe\checkers\cython\setup.py build_ext --inplace --verbose
#C:\Users\Juweriah\pypy\pypy.exe D:\Users\Juweriah\Documents\python\tictactoe\checkers\cython\setup.py build_ext --inplace --verbose
#C:\Users\Juweriah\pypy\pypy.exe main.py
#C:\Users\Juweriah\pypy\pypy.exe checkers\cython\main.py

#C:\Users\Juweriah\pypy\pypy.exe setup.py clean --all
#C:\Users\Juweriah\pypy\pypy.exe setup.py build_ext --inplace

#C:\Users\Juweriah\pypy\pypy.exe -m cProfile  main.py
