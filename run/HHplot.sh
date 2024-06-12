TAG="2023Dec7_binMYx2_addMX650_10ev_unblind_SR"
# TAG="2023Dec7_binMYx2_addMX650_10ev_fullPlane_SR"
unblind="--unblind"
ayear="RunII"; python3 src/PlotLimitVsMy_orig.py --tag ${TAG} --systematics --year ${ayear} ${unblind} --vsMY
