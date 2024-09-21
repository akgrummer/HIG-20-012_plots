sig_NMSSM_bbbb_MX_700_MY_300

copied hists from the fillHists for paper plots

rootcp -r VarPlots/rootHists/fullSubmission_2022Nov/2018DataPlots_2023Dec7_binMYx2_addMX650_10ev_fullPlane/outPlotter.root:sig_NMSSM_bbbb_MX_700_MY_300/selectionbJets_SignalRegion/sig_NMSSM_bbbb_MX_700_MY_300_selectionbJets_SignalRegion_HH_kinFit_m_H2_m paperHists.root

rootcp -r VarPlots/rootHists/fullSubmission_2022Nov/2018DataPlots_2023Dec7_binMYx2_addMX650_10ev_fullPlane/outPlotter.root:sig_NMSSM_bbbb_MX_700_MY_300/selectionbJets_SignalRegion/data_BTagCSV_selectionbJets_SignalRegion_HH_kinFit_m_H2_m paperHists.root

rootcp -r VarPlots/rootHists/fullSubmission_2022Nov/2018DataPlots_2023Dec7_binMYx2_addMX650_10ev_fullPlane/outPlotter.root:data_BTagCSV_dataDriven_kinFit/selectionbJets_SignalRegion/data_BTagCSV_dataDriven_kinFit_selectionbJets_SignalRegion_HH_kinFit_m_H2_m paperHists.root


Plot hists:
python3 src/plotDistributions.py --year 2018

different signal for the paper:
rootcp -r VarPlots/rootHists/fullSubmission_2022Nov/2018DataPlots_2023Dec7_binMYx2_addMX650_10ev_fullPlane/outPlotter.root:sig_NMSSM_bbbb_MX_700_MY_400/selectionbJets_SignalRegion/sig_NMSSM_bbbb_MX_700_MY_400_selectionbJets_SignalRegion_HH_kinFit_m_H2_m VarPlots/paperHists.root


To make plots:

1. 1D distributions:
python3 src/plot1Dvars.py
(uses src/VariableDicts.py)

2. 2D distributions:
python3 src/plotDistributions.py --year 2018

3. all limits:
./run/multiPadPlots.sh

4. X->HH limits:
./run/HHplot.sh

5. 2d limits vs theory:
./run/theoryComparison.sh


./run/createNMSSMrootfile.sh




