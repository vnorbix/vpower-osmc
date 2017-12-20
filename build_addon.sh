#!/bin/bash

PYENV_PACKAGES="pyenv/lib/python2.7/site-packages"

# Interrupt script on any error
set -e

# Cleanup
rm -rf build
rm -rf pyenv
rm -rf dist
mkdir build
mkdir dist

# Create PIP env with dependencies
if [ ! -d pyenv ]; then
    virtualenv -p python2 pyenv
fi
. pyenv/bin/activate
# This is needed, otherwise pip install will throw an error:
# ImportError: No module named _markerlib
easy_install distribute
pip install -r vpower/requirements.txt

# Copy dependencies
cp -rv addon/* build/
cp -rv "$PYENV_PACKAGES/ant" build/
cp -rv "$PYENV_PACKAGES/msgpack" build/
cp -rv "$PYENV_PACKAGES/serial" build/
cp -rv "$PYENV_PACKAGES/usb" build/
cp -rv "vpower" build/
# Allow vpower to be used as module
touch "build/vpower/__init__.py"
rm -rv "build/vpower/.git" "build/vpower/.gitignore"

# Patch ANT+
patch -p0 < ant_driver.patch

# Patch Vpower config
patch -p0 < vpower_config.patch

# Create addon zip
# find build/ -iname "*.pyc" -exec rm -v {} \;
zip -r dist/vpower.zip build/*