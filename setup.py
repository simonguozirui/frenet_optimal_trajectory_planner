from setuptools import Distribution
import setuptools.command.build_ext as _build_ext
from distutils.core import setup, Extension
import sysconfig
from pathlib import Path
import sys
import subprocess
# from Cython.Build import cythonize


# Reference: https://docs.python.org/3.6/extending/building.html

# class build_ext(_build_ext.build_ext):
#     def run(self):
#             command = ["./build.sh", "-p", sys.executable]
#             subprocess.check_call(command)

# class BinaryDistribution(Distribution):
#     def has_ext_modules(self):
#         return True

def main():
    CFLAGS = ['-std=c++11', '-march=native', '-I', '-O3', '-pthread', '-Wall'] #$ANACONDA_HOME/bin/python
    LDFLAGS = ["-I", '/usr/include/eigen3', '-l', 'eigen3']

    # module = Extension('fot_planner',
    #                 sources = ['src/FrenetOptimalTrajectory/planner_package.cpp'
    #                 # 'src/FrenetOptimalTrajectory/AnytimeFrenetOptimalTrajectory.cpp',
    #                 # 'src/CubicSpline/CubicSpline1D.cpp',
    #                 # 'src/CubicSpline/CubicSpline2D.cpp'
    #                 ],
    #                 extra_compile_args = CFLAGS)
    #                 # include_dirs = ["src/CublicSpline/"])
    #                 # extra_link_args = LDFLAGS)

    sources = [
            'src/FrenetOptimalTrajectory/planner_package.cpp',
            'src/Polynomials/QuarticPolynomial.cpp',
            'src/Polynomials/QuinticPolynomial.cpp',
            'src/CubicSpline/CubicSpline1D.cpp',
            'src/CubicSpline/CubicSpline2D.cpp',
            'src/FrenetOptimalTrajectory/FrenetOptimalTrajectory.cpp',
            'src/FrenetOptimalTrajectory/AnytimeFrenetOptimalTrajectory.cpp',
            'src/FrenetOptimalTrajectory/FrenetPath.cpp',
            'src/FrenetOptimalTrajectory/fot_wrapper.cpp',
            'src/Obstacle/Obstacle.cpp',
            'src/Car/Car.cpp']

    #sources = ['src/FrenetOptimalTrajectory/planner_package.cpp']
    module = Extension('fot_planner', sources = sources, 
                            language='C++',
                            include_dirs=['/src', '/src/CubicSpline', '/src/Polynomials', '/src/FrenetOptimalTrajectory', '/src/Obstacle', '/src/Car'],
                            extra_compile_args = CFLAGS, 
                        )

    setup(name="fot_planner",
        version="1.0.0",
        description="FOT Planner",
        author="ERDOS Project",
        # cmdclass={"build_ext": build_ext},
        # distclass= BinaryDistribution,
        ext_modules=[module]
        # ext_modules= cythonize([module])
        )

        

if __name__ == "__main__":
    main()