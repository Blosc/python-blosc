#!/bin/bash

set -x

versions=(cp27-cp27m cp27-cp27mu cp35-cp35m cp36-cp36m cp37-cp37m)

for version in "${versions[@]}"; do
  /opt/python/${version}/bin/python -m pip install --upgrade pip
  /opt/python/${version}/bin/python -m pip install numpy psutil ninja cmake scikit-build auditwheel
  /opt/python/${version}/bin/python setup.py --build-type Release bdist_wheel
done

for whl in dist/*linux_*.whl; do
  /opt/python/cp37-cp37m/bin/auditwheel repair ${whl} -w /work/dist/
  rm ${whl}
done

for version in "${versions[@]}"; do
  pybin=/opt/python/${version}/bin/python
  ${pybin} -m pip install --user numpy
  cd /tmp/
  ${pybin} -m pip install blosc --user --no-cache-dir --no-index -f /work/dist/
  cd /work/
  ${pybin} blosc/test.py
done
