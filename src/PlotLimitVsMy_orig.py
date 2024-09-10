from ROOT import TH2D, TCanvas, TFile, TGraphAsymmErrors, TGraph, TLegend, TLatex, TColor, gPad
import ROOT
import subprocess
from array import array
import os
import argparse
import os.path
from array import array


ROOT.gROOT.SetBatch(True)

colorObs=TColor.GetColor('#F0240Bff')
colorExp=ROOT.kBlack
color1sig=TColor.GetColor('#85D1FBff')
color2sig=TColor.GetColor('#FFDF7Fff')

parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--tag'    , dest = 'tag'    , help = 'tag file' , required = True)
parser.add_argument('--systematics'   , dest='systematics'   , help='systematics'   , action="store_true", default = False, required = False)
parser.add_argument('--year'   , dest='year'   , help='run year, 2016,2017,2018,RunII', default = "RunII", required = False)
parser.add_argument('--vsMY', dest='vsMY', default=False, action='store_true', required=False)
parser.add_argument('--unblind'   , dest='unblind'   , help='plot the observed graph also', action='store_true', default = False, required = False)

args = parser.parse_args()

append = "statOnly"
if args.systematics : append = "syst"

#  xMassList = [300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1400, 1600, 1800, 2000]
xMassList = [400, 500, 600, 650, 700, 800, 900, 1000, 1100, 1200, 1400, 1600]
# yMassList = [60, 70, 80, 90, 100, 125, 150, 200, 250, 300, 400, 500,600, 700, 800, 900, 1000, 1200, 1400]
yMassList = [125]

if args.vsMY:
    massList = yMassList
    massXY = "Y"
    othermassXY="X"
else:
    massList = xMassList
    massXY = "X"
    othermassXY="Y"

ifile="hists/Limits_{0}.root".format(args.tag)
inputFile = TFile(ifile)

for theMass in massList:
    theCanvas = TCanvas("limitMapCentral", "limitMapCentral", 800, 800)
    gPad.SetMargin(0.16,0.05,0.12,0.05)
    ROOT.gStyle.SetOptStat(0) # remove the stats box
    ROOT.gStyle.SetOptTitle(0) # remove the title
    theCanvas.SetLogy()
    theCanvas.SetTicks(1,1)
    # theLegend.SetNColumns(2);


    inputGraph2sigmaName = "Limits_{0}/Option_{1}/2SigmaLimit_{0}_{1}_mass{2}_{3}".format(args.year, append, massXY, theMass)
    # print("here", inputGraph2sigmaName)
    theGraph2sigma = inputFile.Get(inputGraph2sigmaName)
    theGraph2sigma.SetTitle("")
    theGraph2sigma.GetXaxis().SetTitle("m_{%sreco} [GeV]"%(othermassXY))
    theGraph2sigma.GetXaxis().SetLabelFont(62)
    theGraph2sigma.GetXaxis().SetLabelSize(0.045)
    theGraph2sigma.GetXaxis().SetTitleFont(62)
    theGraph2sigma.GetXaxis().SetTitleSize(0.045)
    theGraph2sigma.GetYaxis().SetLabelFont(62)
    theGraph2sigma.GetYaxis().SetLabelSize(0.045)
    theGraph2sigma.GetYaxis().SetTitleFont(62)
    theGraph2sigma.GetYaxis().SetTitleSize(0.045)
    theGraph2sigma.GetYaxis().SetTitle("#sigma(pp #rightarrow X) #times BR(H(b#bar{b}) H(b#bar{b})) [fb]")
    theGraph2sigma.GetYaxis().SetRangeUser(5e-1,1.e5)
    theGraph2sigma.GetXaxis().SetRangeUser(50.,1900.)
    theGraph2sigma.SetTitle("m_{%s} = %i GeV"%(massXY,theMass))
    theGraph2sigma.SetFillColor(color2sig)
    theGraph2sigma.Draw("a3")

    inputGraph1sigmaName = "Limits_{0}/Option_{1}/1SigmaLimit_{0}_{1}_mass{2}_{3}".format(args.year, append, massXY, theMass)
    theGraph1sigma = inputFile.Get(inputGraph1sigmaName)
    theGraph1sigma.SetFillColor(color1sig)
    theGraph1sigma.Draw("same 3")

    inputGraphName = "Limits_{0}/Option_{1}/CentralLimit_{0}_{1}_mass{2}_{3}".format(args.year, append, massXY, theMass)
    theGraph = inputFile.Get(inputGraphName)

    theGraph.SetLineColor(colorExp)
    theGraph.SetLineStyle(7)
    theGraph.SetMarkerColor(colorExp)
    theGraph.SetLineWidth(2)
    theGraph.SetMarkerStyle(22)
    theGraph.SetMarkerSize(0.7)
    theGraph.Draw("same l")

    ATLASn = 5
    ATLASx = array('d', [ 400, 500, 600, 800, 1000 ])
    ATLASy = array('d', [ 89.33, 30.52, 15.38, 5.39, 2.71 ])
    ATLASgraph = TGraph(ATLASn,ATLASx,ATLASy)
    ATLASgraph.SetMarkerStyle(26)
    ATLASgraph.SetMarkerColor(ROOT.kBlack)
    ATLASgraph.Draw("same p")

    for i in range(theGraph.GetN()):
        print("x: ", theGraph.GetPointX(i), "y:", theGraph.GetPointY(i) )

    inputGraphName = "Limits_{0}/Option_{1}/ObservedLimit_{0}_{1}_mass{2}_{3}".format(args.year, append, massXY, theMass)
    theGraphObserved = inputFile.Get(inputGraphName)
    theGraphObserved.SetLineColor(colorObs)
    theGraphObserved.SetLineStyle(1)
    theGraphObserved.SetMarkerColor(colorObs)
    theGraphObserved.SetLineWidth(2)
    theGraphObserved.SetMarkerStyle(20)
    theGraphObserved.SetMarkerSize(0.7)
    if (args.unblind): theGraphObserved.Draw("same l")

    theGraph2sigma.GetYaxis().SetTitleOffset(1.8)

    CMSlabel = TLatex()
    CMSlabel.SetTextFont(63)
    CMSlabel.SetTextSize( 30 )
    # CMSlabel.DrawLatexNDC(0.16, 0.96, "CMS #scale[0.8]{#it{#bf{Work In Progress}}}")
    CMSlabel.DrawLatexNDC(0.16, 0.96, "CMS")

    plotlabels = TLatex()
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(20)
    plotlabels.DrawLatexNDC(0.25, 0.9, "X#rightarrow HH")
    plotlabels.SetTextFont(43)
    plotlabels.SetTextSize(20)
    if("RunII" in args.year): yearLabel="138 fb^{-1} (13 TeV)"
    plotlabels.DrawLatexNDC(0.76, 0.96, yearLabel)


    theLegend  = TLegend(0.2,0.7,0.5,0.88)
    theLegend.AddEntry(theGraph, "Expected 95% upper limit", "l")
    if (args.unblind): theLegend.AddEntry(theGraphObserved, "Observed 95% upper limit", "l")
    theLegend.AddEntry(theGraph1sigma, "Expected limit #pm1 #sigma", "f" )
    theLegend.AddEntry(theGraph2sigma, "Expected limit #pm2 #sigma", "f" )
    theLegend.AddEntry(ATLASgraph, "ATLAS Expected Estimate", "p" )
    theLegend.SetBorderSize(0) # remove the border
    theLegend.SetLineColor(0)
    theLegend.SetFillColor(0)
    theLegend.SetTextSize(0.028)
    theLegend.SetFillStyle(0) # make the legend background transparent
    theLegend.Draw("same")

    odir = "results/Limits_vsm{0}/".format(massXY)
    if not os.path.isdir(odir):
        os.mkdir(odir)

    # odir = "results/Limits_{0}/".format(args.tag)
    # if not os.path.isdir(odir):
    #     os.mkdir(odir)
    # if (args.unblind): odir = "{0}{1}/".format(odir,"unblinded")
    # else: odir = "{0}{1}/".format(odir,"blinded")
    # if not os.path.isdir(odir):
    #     os.mkdir(odir)
    # odir = "{0}{1}/".format(odir,"vsm{0}".format(massXY))
    # if not os.path.isdir(odir):
    #     os.mkdir(odir)
    # odir = "{0}{1}/".format(odir,args.year)
    # if not os.path.isdir(odir):
    #     os.mkdir(odir)

    # N_points = theGraph.GetN()
    # x, y = ROOT.Double(0), ROOT.Double(0)
    # multiplier = ROOT.Double(1)
    # print(N_points)
    # with open(odir+'limitValues.txt', mode='a') as f:
    #     f.write("{}\n".format(args.year))
    #     for i in xrange(N_points):
    #         theGraph.GetPoint(i, x, y)
    #         if theMass<600: multiplier = 100
    #         elif theMass<1600: multiplier = 10
    #         else: multiplier = 1
    #         r = y/multiplier
    #         f.write("MX = {0} MY = {1}: Cent Exp. r val = {2:.2f}\n".format(theMass,x,r))


    theCanvas.SaveAs(odir+"eLimits_m{0}_{1}.pdf".format(massXY, theMass))
    del theCanvas

inputFile.Close()
