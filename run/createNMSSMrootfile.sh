g++  -std=c++17 -I `root-config --incdir`  -o bin/NMSSMrootfile  src/NMSSMrootfile.C `root-config --libs` -O3

./bin/NMSSMrootfile
