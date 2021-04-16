from setuptools import Distribution
import setuptools.command.build_ext as _build_ext
from distutils.core import setup, Extension
import sysconfig
from pathlib import Path
import sys
import subprocess

# Reference: https://docs.python.org/3.6/extending/building.html

# eigen_path = Path('Eigen')
eigen_path = Path('/usr/include/eigen3')

class build_ext(_build_ext.build_ext):
    def run(self):
            command = ["./build.sh", "-p", sys.executable]
            subprocess.check_call(command)

class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True

def main():
    CFLAGS = ['-march=native', '-O3', '-pthread', '-Wall']
    # LDFLAGS = ['Eigen3::Eigen']]
    LDFLAGS = []

    # module = Extension('fot_planner',
    #                 sources = ['src/FrenetOptimalTrajectory/planner_package.cpp'
    #                 # 'src/FrenetOptimalTrajectory/AnytimeFrenetOptimalTrajectory.cpp',
    #                 # 'src/CubicSpline/CubicSpline1D.cpp',
    #                 # 'src/CubicSpline/CubicSpline2D.cpp'
    #                 ],
    #                 extra_compile_args = CFLAGS)
    #                 # include_dirs = ["src/CublicSpline/"])
    #                 # extra_link_args = LDFLAGS)

    # module = Extension('fot_planner', sources = ['src/FrenetOptimalTrajectory/planner_package.cpp'], 
                            # extra_compile_args = CFLAGS)

    setup(name="fot_planner",
        version="1.0.0",
        description="FOT Planner",
        author="ERDOS Project",
        cmdclass={"build_ext": build_ext},
        distclass= BinaryDistribution)
        # ext_modules=[module])

if __name__ == "__main__":
    main()