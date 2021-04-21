#!/bin/bash
sudo apt-get install -y libeigen3-dev clang cmake

# Loop through arguments and process them
for arg in "$@"
do
    case $arg in
        -c|--clean)
        rm -rf fot_planner.egg_info
        rm -rf build
        shift # Remove from processing
        ;;
    esac
done

if [ ! -d "build" ]; then
  mkdir build
fi
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build . --target all -- -j 8
