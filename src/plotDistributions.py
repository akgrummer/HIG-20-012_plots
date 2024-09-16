import ROOT
from ROOT import TFile, TH1F, TH2F, TCanvas, gStyle, gPad, gDirectory, TLatex, gROOT, PyConfig, TMath, kBlue, TLine, TPad, TLegend, TGraph, TBox, kThermometer, THStack, TGraphAsymmErrors
from ROOT import kRed
import numpy as np
import re
import os
import sys
import math
import argparse
import csv

def rootplot_2Dhist(h1, year, tag, descriptionLabel, saveName, ofile):
    c1 = TCanvas('c1', 'c1',800,800)
    gStyle.SetOptStat(0) # remove the stats box
    gStyle.SetOptTitle(0) # remove the title
    # gStyle.SetPalette(kThermometer)
    gPad.SetTicks(1,1)
    # gPad.SetMargin(0.12,0.16,0.12,0.09) #left,right,bottom,top
    gPad.SetMargin(0.16,0.16,0.12,0.05)
    gPad.SetLogz()
    #  p1.SetMargin(0.12,0.05,0.05,0.09) #left,right,bottom,top
    #  p2.SetMargin(0.12,0.05,0.38,0.05) #left,right,bottom,top
    h1.GetXaxis().SetLabelFont(42);
    h1.GetXaxis().SetLabelSize(0.045);
    h1.GetXaxis().SetTitleFont(42);
    h1.GetXaxis().SetTitleSize(0.045);
    h1.GetXaxis().SetNdivisions(505);
    h1.GetYaxis().SetLabelFont(42);
    h1.GetYaxis().SetLabelSize(0.045);
    h1.GetYaxis().SetTitleFont(42);
    h1.GetYaxis().SetTitleSize(0.045);
    h1.GetYaxis().SetTitleOffset(1.8);
    h1.GetZaxis().SetTitleOffset(1.2);
    h1.GetZaxis().SetLabelFont(42);
    h1.GetZaxis().SetLabelSize(0.035);
    h1.GetZaxis().SetTitleFont(42);
    h1.GetZaxis().SetTitleSize(0.045);

    h1.Draw("COLZ1")
    if("Bkg" in saveName): h1.GetZaxis().SetRangeUser(0., 1.29)
    if("Data" in saveName): h1.GetZaxis().SetRangeUser(0., 1.29)
    if("Sig" in saveName): h1.GetZaxis().SetRangeUser(0., 0.0065)
    h1.GetXaxis().SetRangeUser(251., 2000.)
    # h1.GetZaxis().SetTitle("Events/GeV^{2}")
    h1.GetZaxis().SetTitle("Events / GeV^{2}")
    h1.GetXaxis().SetTitle("m_{Xreco} [GeV]")
    h1.GetYaxis().SetTitle("m_{Yreco} [GeV]")

    CMSlabel = TLatex()
    CMSlabel.SetTextFont(63)
    CMSlabel.SetTextSize( 34 )
    # CMSlabel.DrawLatexNDC(0.16, 0.96, "CMS #scale[0.8]{#it{#bf{Work In Progress}}}")
    CMSlabel.DrawLatexNDC(0.2, 0.88, "CMS")
    plotlabels = TLatex()

    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(20)
    labelText = "Signal Region"
    plotlabels.DrawLatexNDC(0.2, 0.84, labelText)

    plotlabels.SetTextFont(53)
    plotlabels.SetTextSize(20)
    plotlabels.DrawLatexNDC(0.2, 0.81, descriptionLabel)

    plotlabels.SetTextFont(43)
    plotlabels.SetTextSize(20)
    # mXval = sig.split("MX_")[1].split("_MY_")[0]
    # mYval = sig.split("MX_")[1].split("_MY_")[1]
    h1.SetMinimum(4e-4)
    if("Sig" in saveName):
        plotlabels.DrawLatexNDC(0.2, 0.78,"m_{{X}} = {0} GeV, m_{{Y}} = {1} GeV".format(700, 400))
        h1.SetMinimum(6e-6)


    plotlabels.SetTextFont(43)
    plotlabels.SetTextSize(25)
    # plotlabels.DrawTextNDC(0.7, 0.96, year)
    if "2016" in year: plotlabels.DrawLatexNDC(0.62, 0.96, "36.3 fb^{-1} (13 TeV)")
    if "2017" in year: plotlabels.DrawLatexNDC(0.62, 0.96, "41.5 fb^{-1} (13 TeV)")
    if "2018" in year: plotlabels.DrawLatexNDC(0.62, 0.96, "59.7 fb^{-1} (13 TeV)")

    odir = "results/"
    if not os.path.isdir(odir):
        os.mkdir(odir)
    c1.SaveAs("{0}{1}.pdf".format(odir, saveName))

    del c1
    del h1

def DivideBinArea(h):
    for binx in range(1,h.GetNbinsX()):
        for biny in range(1,h.GetNbinsY()):
                h.SetBinContent(binx,biny,
                h.GetBinContent(binx,biny) /(h.GetYaxis().GetBinWidth(biny) *h.GetXaxis().GetBinWidth(binx))
            )
    return h

def getNoneZeroBins(h, h2, valueToSet):
    nXbin = h.GetNbinsX();
    nYbin = h.GetNbinsY();
    for yBin in range(nYbin):
        for xBin in range(nXbin):
            # mX = h.GetXaxis().GetBinCenter(xBin);
            # mY = h.GetYaxis().GetBinCenter(yBin);
            binContent = h.GetBinContent(xBin,yBin)
            binContent2 = h2.GetBinContent(xBin,yBin)
            h.SetBinContent(xBin,yBin, 0)
            if (binContent > 0 and binContent2<valueToSet): h2.SetBinContent(xBin,yBin, valueToSet)
    return h


def lowStatsBinCut(h):
    nXbin = h.GetNbinsX();
    nYbin = h.GetNbinsY();
    for yBin in range(nYbin):
        for xBin in range(nXbin):
            mX = h.GetXaxis().GetBinCenter(xBin);
            mY = h.GetYaxis().GetBinCenter(yBin);
            # attempt to show correct bins cuts in the plots:
            # binContent = h.GetBinContent(xBin,yBin)
            # if (binContent == 0 and mX-mY>=125 and mX>400): h.SetBinContent(xBin,yBin, 1e-5)
            if( mX > 1678 and mY < 770 ): h.SetBinContent(xBin,yBin, 0)
            if( mX > 1550 and mY < 205 ): h.SetBinContent(xBin,yBin, 0)
            if( mX > 1423 and mY < 141 ): h.SetBinContent(xBin,yBin, 0)
            if( mX > 959 and mY < 52): h.SetBinContent(xBin,yBin, 0)
    return h


def makePlotsPerYear(year, ifileName, ofile):

    inFile = ROOT.TFile(ifileName)

    hSig = inFile.sig_NMSSM_bbbb_MX_700_MY_400_selectionbJets_SignalRegion_HH_kinFit_m_H2_m
    hData = inFile.data_BTagCSV_selectionbJets_SignalRegion_HH_kinFit_m_H2_m
    hBkg     = inFile.data_BTagCSV_dataDriven_kinFit_selectionbJets_SignalRegion_HH_kinFit_m_H2_m

    hSig = DivideBinArea(hSig)
    hData = DivideBinArea(hData)
    hBkg = DivideBinArea(hBkg)

    hSig = lowStatsBinCut(hSig)
    hData = lowStatsBinCut(hData)
    hBkg = lowStatsBinCut(hBkg)
    # hSig.Add(hBkg)
    ###########
    # this part is to add lowest z color for bins that are populated in the analysis
    # use bkg hist as reference for all bins
    hTempData =hBkg.Clone("hTempData")
    hTempData = getNoneZeroBins(hTempData, hData, 5e-4)
    hTempBkg =hBkg.Clone("hTempBkg")
    hTempBkg = getNoneZeroBins(hTempBkg, hBkg, 5e-4)
    hTempSig =hBkg.Clone("hTempSig")
    hTempSig = getNoneZeroBins(hTempSig, hSig, 6e-6)
    # hSig.Add(hTempSig)
    # hData.Add(hTempData)
    # hBkg.Add(hTempBkg)
    ###############


    rootplot_2Dhist(hData, year, "tag",
                    "Data distribution",
                    "aData",
                    ofile
                    )

    rootplot_2Dhist(hSig, year, "tag",
                    "Signal distribution",
                    "cSignal",
                    ofile
                    )

    rootplot_2Dhist(hBkg, year, "tag",
                    "Bkg. model distribution",
                    "bBkg",
                    ofile
                    )


    del hSig
    del hData
    del hBkg

##################################################
gROOT.SetBatch(True)
parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--year'  ,  dest = 'year'   ,  help = 'production tag'  ,  default = ""  ,  required = True  )

args = parser.parse_args()

ifile = "input/paperHists.root"
ofile = ""

makePlotsPerYear("{}".format(args.year), ifile, ofile)

