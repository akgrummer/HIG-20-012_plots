import ROOT
from ROOT import TFile, TH1F, TH2F, TCanvas, gStyle, gPad, gDirectory, TLatex, gROOT, PyConfig, TMath, kBlue, TLine, TPad, TLegend, TGraph, TBox, kThermometer, THStack, TGraphAsymmErrors
from ROOT import kRed
# PyConfig.IgnoreCommandLineOptions = False
import numpy as np
import re
import os
from VariableDicts import varInfo
import sys
import math

def rootplot_2samp_ratio( h1, h2, year, region, var, tag, odir, h_up, h_down ):

    #### get the histograms:
    # get the 4b hist
    # h1.Rebin(2)
    # h2.Rebin(2)
    # h_up.Rebin(2)
    # h_down.Rebin(2)
    h4 = h2.Clone("h4")

    # determine the stat err / bin content for 4b hist
    for i in range(h2.GetSize()):
        if (h4.GetBinContent(i)>0): h4.SetBinError(i,h4.GetBinError(i)/h4.GetBinContent(i))
        else: h4.SetBinError(i,0)
        # h4.SetBinContent(i,1)

    # get the 3b hist, and start computing the shape uncertainties
    h3 = h1.Clone("h3")
    # hshape1 = h_up.Clone("hshape1")
    # hshape2 = h_up.Clone("hshape2")
    # need a TGraph to account for possible asymmetric uncetainties in the shape
    gr = TGraphAsymmErrors(h3.GetSize())
    gr.SetPointError(0, h3.GetXaxis().GetBinWidth(1)/2, h3.GetXaxis().GetBinWidth(1)/2, 0, 0 )# i, exl, exh, eyl, eyh
    gr.SetPoint(0, -1, 1)
    gr1 = TGraphAsymmErrors(h3.GetSize())
    gr1.SetPointError(0, h3.GetXaxis().GetBinWidth(1)/2, h3.GetXaxis().GetBinWidth(1)/2, 0, 0 )# i, exl, exh, eyl, eyh
    gr1.SetPoint(0, -1, 1)

    # set the bin content of the graph from the shape differences w.r.t 3b hist (one must be up and one must be down)
    for i in range(h3.GetSize()):
        x = h3.GetXaxis().GetBinCenter(i)
        stat_err = h3.GetBinError(i)
        dist_1 = np.abs(h_up.GetBinContent(i) - h3.GetBinContent(i))
        dist_2 = np.abs(h_down.GetBinContent(i) - h3.GetBinContent(i))
        max_shape = np.max([dist_1, dist_2])
        shape_err_up = max_shape
        shape_err_down = max_shape
        if (62<x and x<188): nonclosure = h3.GetBinContent(i)*0.1
        else: nonclosure=0
        # if ( hshape1.GetBinContent(i) >= h3.GetBinContent(i)):
        #     shape_err_up = hshape1.GetBinContent(i) - h3.GetBinContent(i)
        #     # print("shape_err_up:",shape_err_up)
        #     shape_err_down = h3.GetBinContent(i) - hshape2.GetBinContent(i)
        # else:
        #     shape_err_up = hshape2.GetBinContent(i) - h3.GetBinContent(i)
        #     # print("shape_err_up:",shape_err_up)
        #     shape_err_down = h3.GetBinContent(i) - hshape1.GetBinContent(i)
        norm_err = h3.GetBinContent(i)*0.04
        if (h3.GetBinContent(i)>0):
            h3.SetBinError(i,h3.GetBinError(i)/h3.GetBinContent(i))
            bin_err_up = math.sqrt(stat_err**2 + shape_err_up**2 + norm_err**2 + nonclosure**2)/h3.GetBinContent(i)
            bin_err_down = math.sqrt(stat_err**2 + shape_err_down**2 + norm_err**2 + nonclosure**2)/h3.GetBinContent(i)
            bin_err_up_1 = math.sqrt(stat_err**2 + shape_err_up**2 + norm_err**2 + nonclosure**2)/h3.GetXaxis().GetBinWidth(i)
            bin_err_down_1 = math.sqrt(stat_err**2 + shape_err_down**2 + norm_err**2 + nonclosure**2)/h3.GetXaxis().GetBinWidth(i)
            # print("stat/bincontent {0:.3f} shape_up {1:.3f} norm {2:.3f}, bin_err_up {3:.3f}".format(stat_err/h3.GetBinContent(i), shape_err_up, norm_err, bin_err_up))

        else:
            h3.SetBinError(i,0)
            bin_err_up = 0
            bin_err_down = 0
            bin_err_up_1 = 0
            bin_err_down_1 = 0

        # if (5<i and i<10):
        #     print("statErr:", h3.GetBinError(i))
        #     print("upErr:", bin_err_up)
        # if (i>10):sys.exit()
        #  use the i+1 for the graph def to avoid the underflow bin
        # # gr.SetPointError(i+1, h3.GetXaxis().GetBinWidth(i)/2, h3.GetXaxis().GetBinWidth(i)/2, h3.GetBinError(i), h3.GetBinError(i))# i, exl, exh, eyl, eyh
        gr.SetPointError(i+1, h3.GetXaxis().GetBinWidth(i)/2, h3.GetXaxis().GetBinWidth(i)/2, bin_err_down, bin_err_up)# i, exl, exh, eyl, eyh
        gr1.SetPointError(i+1, h3.GetXaxis().GetBinWidth(i)/2, h3.GetXaxis().GetBinWidth(i)/2, bin_err_down_1, bin_err_up_1)# i, exl, exh, eyl, eyh
        h3.SetBinContent(i,1)
        # # use the i+1 for the graph def to avoid the underflow bin
        gr.SetPoint(i+1, x, 1)
    h1 = h1.Clone("h1copy")
    h2 = h2.Clone("h2copy")
    # href = href.Clone("hrefcopy")

    # normalize histograms
    #  h1.Sumw2()
    #  h2.Sumw2()
    h1area = h1.Integral(0,-1)
    h2area = h2.Integral(0,-1)
    # normalize by bin width
    for i in range(h3.GetSize()):
        x = h3.GetXaxis().GetBinCenter(i)
        h1.SetBinContent(i, h1.GetBinContent(i)/h1.GetBinWidth(i))
        h2.SetBinContent(i, h2.GetBinContent(i)/h2.GetBinWidth(i))
        h2.SetBinError(i, h2.GetBinError(i)/h2.GetBinWidth(i))
        gr1.SetPoint(i+1, x, h1.GetBinContent(i))
        # hshape1.SetBinContent(i, hshape1.GetBinContent(i)/hshape1.GetBinWidth(i))
        # hshape2.SetBinContent(i, hshape2.GetBinContent(i)/hshape2.GetBinWidth(i))
    # remove all normalization effect (accounted for in a ~3% uncertainty, Appendix D in the note)
    # h1.Scale(1./h1.Integral())
    # h2.Scale(1./h2.Integral())
    # href.Scale(1./href.Integral())

    #### define the canvas
    c1 = TCanvas('c1', 'c1',800,700)
    gStyle.SetOptStat(0) # remove the stats box
    gStyle.SetOptTitle(0) # remove the title

    #### define the upper and lower pads
    p1 = TPad("p1", "p1", 0., 0.3, 1., 1.0, 0, 0, 0)
    p1.SetMargin(0.12,0.05,0.05,0.09) #left,right,bottom,top
    p1.SetTicks(1,1)
    p1.Draw()

    p2 = TPad("p2", "p2", 0., 0.05, 1., 0.3, 0, 0, 0)
    p2.SetMargin(0.12,0.05,0.38,0.05) #left,right,bottom,top
    p2.SetTicks(1,1)
    p2.Draw()

    #### draw histograms in upper pad
    p1.cd()
    h1.SetLineColor(kRed+2)
    h1.SetLineWidth(2)
    h2.SetLineColor(ROOT.kAzure+2)
    h2.SetLineWidth(2)
    h2.SetMarkerStyle(22)
    h2.SetMarkerSize(0.6)
    h2.SetMarkerColor(1)
    # hshape1.SetLineColor(1)
    # hshape1.SetLineWidth(2)
    # hshape2.SetLineColor(1)
    # hshape2.SetLineWidth(2)
    gr1.SetLineColor(2);
    gr1.SetLineWidth(4);
    gr1.SetFillColor(ROOT.kRed-6);
    # gr1.SetFillColor(1);
    gr1.SetMarkerColor(1);
    gr1.SetMarkerSize(0.);
    gr1.SetMarkerStyle(20);
    h1.Draw("hist")
    gr1.Draw("2")
    h1.Draw("hist same")
    h2.Draw("same")
    # hshape1.Draw("hist same")
    # hshape2.Draw("hist same")
    #xaxis
    # h1.GetXaxis().SetRangeUser(varInfo[var]['xlowRange'],varInfo[var]['xhighRange'])
    # h1.GetXaxis().SetRangeUser(0,800)
    # h1.GetXaxis().SetRangeUser(450,2500)
    h1.GetXaxis().SetLabelSize(0.)
    h1.GetXaxis().SetTitleSize(0.)
    # h2.GetXaxis().SetRangeUser(varInfo[var]['xlowRange'],varInfo[var]['xhighRange'])
    # h2.GetXaxis().SetRangeUser(0,800)
    # h2.GetXaxis().SetRangeUser(450,2500)
    h2.GetXaxis().SetLabelSize(0.)
    h2.GetXaxis().SetTitleSize(0.)
    # hshape1.GetXaxis().SetRangeUser(varInfo[var]['xlowRange'],varInfo[var]['xhighRange'])
    # hshape1.GetXaxis().SetRangeUser(0,800)
    # hshape1.GetXaxis().SetRangeUser(450,2500)
    # hshape1.GetXaxis().SetLabelSize(0.)
    # hshape1.GetXaxis().SetTitleSize(0.)
    # hshape2.GetXaxis().SetRangeUser(varInfo[var]['xlowRange'],varInfo[var]['xhighRange'])
    # hshape2.GetXaxis().SetRangeUser(0,800)
    # hshape2.GetXaxis().SetRangeUser(450,2500)
    # hshape2.GetXaxis().SetLabelSize(0.)
    # hshape2.GetXaxis().SetTitleSize(0.)
    #yaxis
    if var == "HH_kinFit_m" or var == "H2_m": h1.GetYaxis().SetTitle(varInfo[var]['YaxisTitle'] + "/bin")
    else: h1.GetYaxis().SetTitle(varInfo[var]['YaxisTitle'])
    h1.GetYaxis().SetLabelFont(62)
    h1.GetYaxis().SetLabelSize(0.05)
    h1.GetYaxis().SetTitleFont(63)
    h1.GetYaxis().SetTitleSize(30)
    h1.GetYaxis().SetTitleOffset(1.3)
    h1.GetYaxis().SetTickLength(0.02)
    if var == "HH_kinFit_m" or var == "H2_m": h2.GetYaxis().SetTitle(varInfo[var]['YaxisTitle']+"/bin")
    else: h2.GetYaxis().SetTitle(varInfo[var]['YaxisTitle'])
    h2.GetYaxis().SetLabelFont(62)
    h2.GetYaxis().SetLabelSize(0.05)
    h2.GetYaxis().SetTitleFont(63)
    h2.GetYaxis().SetTitleSize(30)
    h2.GetYaxis().SetTitleOffset(1.3)
    h2.GetYaxis().SetTickLength(0.02)
    #  if h2.GetMaximum()>h1.GetMaximum():
    yrangeFactor = 1.3
    if var == "HH_kinFit_m": yrangeFactor = 1.57
    #  h1.GetYaxis().SetRangeUser(0,np.max( [ h1.GetMaximum(), h2.GetMaximum(), href.GetMaximum() ] )*yrangeFactor)
    h1.GetYaxis().SetRangeUser(0,np.max( [ h2.GetMaximum()] )*yrangeFactor)
    # h1.GetYaxis().SetRangeUser(0,np.max( [ h1.GetMaximum(), h2.GetMaximum(), hshape1.GetMaximum(), hshape2.GetMaximum()] )*yrangeFactor)

    ### KStest and AD test
    ksval = "KS Test: %.4f"%h1.KolmogorovTest(h2)
    # print("KS test, UO %e"%h1.KolmogorovTest(h2, "UO"))
    ksvalMaxDist= "KS Test, Max Dist.: %.4f"%h1.KolmogorovTest(h2, "M")
    # print("KS test, normalized %e"%h1.KolmogorovTest(h2, "N"))
    ksvalX = "KS Test, pseudoX: %.4f"%h1.KolmogorovTest(h2, "X")
    # print("AD test %e"%h1.AndersonDarlingTest(h2))
    # print("AD test, normalized %e"%h1.AndersonDarlingTest(h2, "T"))
    CMSlabel = TLatex()
    #  CMSlabel.SetTextSize( 0.08 )
    #  CMSlabel.DrawTextNDC(0.7, 0.85, "CMS Internal")
    CMSlabel.SetTextFont(63)
    CMSlabel.SetTextSize( 34 )
    CMSlabel.DrawLatexNDC(0.12, 0.93, "CMS #scale[0.8]{#it{#bf{Work In Progress}}}")

    plotlabels = TLatex()
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(20)
    #  labelText = "mX = %.0f GeV, mY = %.0f GeV"%(mXval,mYval)
    labelText = ""
    if "VR" in region:    labelText = labelText + "Validation Region"
    if "CR" in region:    labelText = labelText + "Control Region"
    plotlabels.DrawLatexNDC(0.65, 0.93, labelText)
    plotlabels.SetTextFont(73)
    plotlabels.SetTextSize(28)
    plotlabels.DrawTextNDC(0.84, 0.93, year)

    ##### ##### #####
    hErrors = h2.Clone("hErrors")
    hErrors.Divide(h1)
    for i in range(h4.GetSize()):
        h4.SetBinContent(i,hErrors.GetBinContent(i))
    #  for i in xrange( b)
    # h4 = h1.Clone("h4")
    # #  print("number of bins, 3b: ", h1.GetSize())
    # #  print("a bin error %.4f"%(h1.GetBinError(50)))
    # for i in range(h1.GetSize()):
    #     h4.SetBinContent(i,1)
    #     #  print(h1.GetBinError(i))
    hErrors.SetMarkerStyle(20) # marker style (20 = filled circle) that can be resized
    hErrors.SetMarkerSize(0.4)
    hErrors.SetMarkerColor(1)
    hErrors.SetLineColor(1)
    hErrors.SetLineWidth(0)
    h4.SetMarkerStyle(20) # marker style (20 = filled circle) that can be resized
    h4.SetMarkerSize(0.4)
    h4.SetMarkerColor(1)
    h4.SetLineColor(ROOT.kAzure+2)
    h4.SetLineWidth(2)
    # h4.SetFillColor(ROOT.kRed+1)
    # h4.SetLineColor(17)
    # h4.SetBarWidth(1.)
    h3.SetMarkerStyle(20) # marker style (20 = filled circle) that can be resized
    h3.SetMarkerSize(0.)
    h3.SetMarkerColor(1)
    h3.SetLineColor(1)
    h3.SetLineWidth(0)
    h3.SetFillColor(ROOT.kRed-6)

    #Graph
    gr.SetLineColor(2);
    gr.SetLineWidth(4);
    gr.SetFillColor(ROOT.kRed-6);
    # gr.SetFillColor(1);
    gr.SetMarkerColor(1);
    gr.SetMarkerSize(0.);
    gr.SetMarkerStyle(20);

    #### define legend
    hdummy2 = h2.Clone("hrefcopy")
    hdummy2.SetMarkerStyle(22) # marker style (20 = filled circle) that can be resized
    hdummy2.SetMarkerSize(0.9)
    hdummy2.SetMarkerColor(1)
    leg = TLegend(0.3,0.62,0.55,0.86)
    leg.AddEntry(h1, "3b data (bkg. model)", "l")
    leg.AddEntry(hdummy2, "4b data (target)", "p")
    if (var == "HH_kinFit_m"): modelUnc =  "3b data unc. (stat+shape+norm)"
    else:  modelUnc =  "3b data unc. (stat+shape+norm+non-closure)"
    leg.AddEntry(h3, modelUnc, "f")
    leg.AddEntry(h4, "4b data unc. (stat)", "le")
    #  leg.AddEntry(h1, "3b ttbar", "l")
    #  leg.AddEntry(h2, "4b ttbar", "l")
    # leg.AddEntry(h1, "3b Signal MC", "l")
    # leg.AddEntry(h2, "4b Signal MC", "l")
    leg.SetBorderSize(0) # remove the border
    leg.SetLineColor(0)
    leg.SetFillColor(0)
    leg.SetTextSize(0.05)
    leg.SetFillStyle(0) # make the legend background transparent
    leg.Draw()

    #### draw the ratio hist in lower pad
    p2.cd()
    hErrors.Draw("p") # draw as data points
    # h3.Draw("e2same") # draw as data points
    gr.Draw("2")
    h4.Draw("psame") # draw as data points
    hErrors.Draw("psame") # draw as data points
    #  h3.DrawClone("p same") # draw as data points
    #  h4.Draw("line same")

    #  LineAtOne = TLine(varInfo[var]['xlowRange'],1.,varInfo[var]['xhighRange'],1.) #x1,y1,x2,y2
    LineAtOne = TLine(hErrors.GetXaxis().GetXmin(),1.,hErrors.GetXaxis().GetXmax(),1.) #x1,y1,x2,y2
    LineAtOne.SetLineWidth(2)
    LineAtOne.SetLineColor(1)
    LineAtOne.SetLineStyle(9)
    LineAtOne.Draw()
    #  hErrors.GetYaxis().SetRangeUser(varInfo[var]['xlowRatioRange'],varInfo[var]['xhighRatioRange'])
    #  h4.GetYaxis().SetRangeUser(varInfo[var]['xlowRatioRange'],varInfo[var]['xhighRatioRange'])
    hErrors.GetYaxis().SetRangeUser(0.5, 1.5)
    h4.GetYaxis().SetRangeUser(0.5, 1.5)
    hErrors.GetXaxis().SetLabelFont(62)
    hErrors.GetXaxis().SetLabelSize(0.15)
    hErrors.GetXaxis().SetLabelOffset(0.05)
    hErrors.GetYaxis().SetLabelSize(0.12)
    hErrors.GetYaxis().SetNdivisions(503)
    hErrors.GetXaxis().SetTickLength(0.1)
    hErrors.GetXaxis().SetTitleFont(63)
    hErrors.GetXaxis().SetTitleSize(28)
    hErrors.GetXaxis().SetTitleOffset(1.1)
    hErrors.GetXaxis().SetTitle(varInfo[var]['XaxisTitle'])
    hErrors.GetYaxis().SetTickLength(0.03)
    hErrors.GetYaxis().SetTitleFont(63)
    hErrors.GetYaxis().SetTitleSize(20)
    hErrors.GetYaxis().SetTitleOffset(1.6)
    hErrors.GetYaxis().SetTitle("target / model")
    odir = odir + "/" + region
    if not (os.path.exists(odir)): os.makedirs(odir)
    #  odirpng = odir + "/png"
    #  if not (os.path.exists(odirpng)): os.makedirs(odirpng)
    c1.SaveAs("%s/%s_%s_%s.pdf"%( odir   , var, tag, year ))
    #  c1.SaveAs("%s/%s_%s.png"%( odirpng, var, tag ))

def makeplotsForRegion(dir_region, region, odir, year, ifileTag):
    idir = "hists/{0}DataPlots_{1}".format(year,ifileTag) # outPlotter.root is the same for CR and VR (normal binning)
    odir = odir + year
    myfile = TFile.Open(idir + "/outPlotter.root")
    dir_ttbar_3b = "ttbar_3b"
    dir_ttbar_3b_weights = "ttbar_3bScaled"
    dir_ttbar_4b = "ttbar"
    dir_data_3b = "data_BTagCSV_3btag"
    dir_data_4b = "data_BTagCSV"
    dir_data_3b_weights = "data_BTagCSV_dataDriven_kinFit"
    dir_data_3b_weights_down = "data_BTagCSV_dataDriven_kinFit_down"
    dir_data_3b_weights_up = "data_BTagCSV_dataDriven_kinFit_up"
    dir_QCD = "QCD"
    #  varname = "_HH_kinFit_m_H2_m"

    dir_sig_MX_600_MY_400 = "sig_NMSSM_bbbb_MX_600_MY_400" # signal
    dir_sig_MX_300_MY_60 = "sig_NMSSM_bbbb_MX_300_MY_60" # signal
    dir_sig_MX_300_MY_150 = "sig_NMSSM_bbbb_MX_300_MY_150" # signal
    dir_sig_3b_weights = "sig_NMSSM_bbbb_MX_600_MY_400_3bScaled"
    #  varlist = [ "H1_b1_ptRegressed", "H1_b2_ptRegressed", "H1_b1_kinFit_ptRegressed", "H1_b2_kinFit_ptRegressed", "H2_b1_ptRegressed", "H2_b2_ptRegressed", "H1_b1_deepCSV", "H1_b2_deepCSV", "H2_b1_deepCSV", "H2_b2_deepCSV", "H1_pt", "H1_kinFit_pt", "H2_pt", "HH_m", "HH_kinFit_m", "HH_pt", "HH_kinFit_pt", "H1_m", "H2_m", "H1_eta", "H1_kinFit_eta", "H2_eta", "H1_bb_DeltaR", "H1_kinFit_bb_DeltaR", "H2_bb_DeltaR", "H1_H2_sphericity", "FourBjet_sphericity", "distanceFromDiagonal" ]
    # varlist = [ "H1_b1_kinFit_ptRegressed", "H1_b2_kinFit_ptRegressed", "H2_b1_ptRegressed", "H2_b2_ptRegressed", "H1_kinFit_pt", "H2_pt", "HH_kinFit_m", "HH_kinFit_pt", "H2_m", "H1_kinFit_eta", "H2_eta", "H1_kinFit_bb_DeltaR", "H2_bb_DeltaR", "distanceFromDiagonal" ]
    #  "H1_kinFit_m",
    varlist = [ "H2_m", "HH_kinFit_m"]
    # varlist2D = [ "H1_m_H2_m", "HH_m_H2_m", "HH_kinFit_m_H2_m" ]

    #  masspoint_list = [ "MX_1800_MY_800" ]
    masspoint_list = "MX_600_MY_400"
    sigdirHeader = "sig_NMSSM_bbbb_"
##################################################
#  # data plots
    for varname in varlist:
    #  varname = "H1_b1_kinFit_ptRegressed"
        myfile.cd(dir_data_3b+"/"+dir_region)
        h_3b = gDirectory.Get(dir_data_3b+"_"+dir_region+"_"+varname)
        myfile.cd(dir_data_3b_weights+"/"+dir_region)
        h_3b_weights = gDirectory.Get(dir_data_3b_weights+"_"+dir_region+"_"+varname)
        myfile.cd(dir_data_3b_weights_up+"/"+dir_region)
        h_3b_weights_up = gDirectory.Get(dir_data_3b_weights_up+"_"+dir_region+"_"+varname)
        myfile.cd(dir_data_3b_weights_down+"/"+dir_region)
        h_3b_weights_down = gDirectory.Get(dir_data_3b_weights_down+"_"+dir_region+"_"+varname)
        myfile.cd(dir_data_4b+"/"+dir_region)
        h_4b = gDirectory.Get(dir_data_4b+"_"+dir_region+"_"+varname)
        rootplot_2samp_ratio( h_3b_weights, h_4b, year, region, varname, "weights", odir, h_3b_weights_up, h_3b_weights_down )
##################################################

# ********************
#run pyROOT in batch mode  - ie don't show graphics!
#
gROOT.SetBatch(True)
# ********************
# odir = "VarPlots/2023Feb20_mXmY_shapeUnc_maxShape/"
# odir = "VarPlots/2023Mar2_TrigCut/"
# odir = "VarPlots/2023Feb20_mXmY_shapeUnc_maxShape_oldBinning/"
# odir = "VarPlots/2023Feb20_mXmY_shapeUncRebin/"

# odir = "VarPlots/2023Apr21/"
odir = "results/vars1D/"
years = ["2016","2017","2018"]
#  years = ["2018"]
# !!!!!!!!!!! CAREFUL using Signal Region! !!!!!!!!!!! only for MC
#  directories = ["selectionbJets_SignalRegion"]
#  regionTag = ["SR"]
# !!!!!!!!!!! CAREFUL using Signal Region! !!!!!!!!!!! only for MC
# ##################################################
# for data
# directories = ["selectionbJets_ControlRegionBlinded", "selectionbJets_ValidationRegionBlinded", "selectionbJets_SignalRegion"]
directories = ["selectionbJets_SignalRegion"]
# regionTag = ["CR", "VR", "SR"]
regionTag = ["SR"]
# directories = ["selectionbJets_ControlRegionBlinded", "selectionbJets_ValidationRegionBlinded"]
# regionTag = ["CR", "VR"]
# Old event selections:
# iTags = ["2022Jul7_fullBDT_bJetScoreLoose"]
# iTags = ["2022Nov14_bJetScoreLoose_shapes2"]
# iTags = ["2023Feb22_analysisBinning"]
#New event selections:
# all sigs, few vars:
# iTags = ["2023Feb28_3"]
# few sigs, analysis vars:
# iTags = ["2023Feb28_vars"]
# iTags = ["2023Feb28_hourglass"]
# iTags = ["2023Feb28_vars_sans_mXmY"]
# iTags = ["2023Feb28_vars_only_mXmY"]
# iTags = ["2023Feb28_vars_sans_dfd"]
iTags = ["2024Jun11_vars"]
for iTag in iTags:
   for year in years:
       for i, directory in enumerate(directories):
           #  odir = "studies/plotting2021Dec13/plots2022Jan27/%s"%(year)
           #  year = "2016"
           #  directory = "selectionbJets_ControlRegionBlinded"
           #  makeplotsForRegion(directory, "CR", odir,year)
           #  directory = "selectionbJets_ValidationRegionBlinded"
           makeplotsForRegion(directory, regionTag[i], odir+iTag+"/", year, iTag)
# ##################################################
################################################
#  for MC
#  !!!!!!!!!!! CAREFUL using Signal Region! !!!!!!!!!!! only for MC
#  directories = ["selectionbJets_ControlRegionBlinded", "selectionbJets_ValidationRegionBlinded", "selectionbJets_SignalRion"]
#  regionTag = ["CR", "VR", "SR"]
#  #  iTag="2022Jan26_VR"
#  #  iTag="2022Jul7_fullBDT_bJetScoreLoose"
#  iTag="2022Jul14_fullBDT_bJetScore1p5"
#  for year in years:
    #  # for i, directory in enumerate(directories):
    #  # odir = "studies/plotting2021Dec13/plots2022Jan27/%s"%(year)
    #  # year = "2016"
    #  # directory = "selectionbJets_ControlRegionBlinded"
    #  # makeplotsForRegion(directory, "CR", odir,year)
    #  directory = "selectionbJets_SignalRegion"
    #  makeplotsForRegion(directory, regionTag[2], odir+iTag+"/", year, iTag)

