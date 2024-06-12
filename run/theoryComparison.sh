TAG="2023Dec7_binMYx2_addMX650_10ev_unblind_SR"

g++  -std=c++17 -I `root-config --incdir`  -o bin/Plot2DLimitMap       src/Plot2DLimitMap.C        `root-config --libs` -O3

./bin/Plot2DLimitMap ${TAG}
