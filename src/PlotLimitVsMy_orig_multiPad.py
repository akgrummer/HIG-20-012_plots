from ROOT import TH2D, TCanvas, TFile, TGraphAsymmErrors, TGraph, TLegend, TLatex, TPad, TArrow, TColor
import ROOT
import subprocess
from array import array
import os
import argparse
import os.path
from array import array

def createPad(name, xlow, ylow, xup, yup, margins):
    p = TPad(name, name, xlow, ylow, xup, yup, 0, 0, 0)
    p.SetMargin( margins[0], margins[1], margins[2], margins[3] ) #left,right,bottom,top
    p.SetTicks(1,1)
    p.SetLogy()
    p.Draw()
    return p

def changePad(p):
    p.cd()


colorObs=TColor.GetColor('#F0240Bff')
colorExp=ROOT.kBlack
color1sig=TColor.GetColor('#85D1FBff')
color2sig=TColor.GetColor('#FFDF7Fff')

ROOT.gROOT.SetBatch(True)

parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--tag'    , dest = 'tag'    , help = 'tag file' , required = True)
parser.add_argument('--systematics'   , dest='systematics'   , help='systematics'   , action="store_true", default = False, required = False)
parser.add_argument('--year'   , dest='year'   , help='run year, 2016,2017,2018,RunII', default = "RunII", required = False)
parser.add_argument('--unblind'   , dest='unblind'   , help='plot the observed graph also', action='store_true', default = False, required = False)

args = parser.parse_args()

append = "syst"

#  xMassList = [300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1400, 1600, 1800, 2000]
xMassList = [400, 500, 600, 650, 700, 800, 900, 1000, 1100, 1200, 1400, 1600]
yMassList = [60, 70, 80, 90, 100, 125, 150, 200, 250, 300, 400, 500,600, 700, 800, 900, 1000, 1200, 1400]

massList = xMassList
massXY = "X"
othermassXY="Y"

ifile="hists/Limits_{0}.root".format(args.tag)
inputFile = TFile(ifile)

theCanvas = TCanvas("multiPad", "multiPad", 800, 800)
ROOT.gStyle.SetOptStat(0) # remove the stats box
ROOT.gStyle.SetOptTitle(0) # remove the title
#### define the upper and lower pads
margins = [ 0.12,0.05,0.05,0.09 ] #left,right,bottom,top
margins2 = [ 0.01,0.02,0.20,0.05 ] #left,right,bottom,top
# LeftMargin=0.10
LeftMargin=0.20
margins3 = [ LeftMargin,0.02,0.20,0.05 ] #left,right,bottom,top
start = [0.04, 0.75]
startXMargin1=start[0]+0.045
startXMargin2=start[0]+0.021
offsetX = 0.31
offsetY = 0.20
p1   = createPad(  "p1",  start[0],                start[1],           startXMargin1+offsetX    , start[1]+offsetY  , margins3 ) # xlow, ylow, xup, yup
p2   = createPad(  "p2",  startXMargin1+offsetX,   start[1],           startXMargin2+offsetX*2  , start[1]+offsetY  , margins2 ) # xlow, ylow, xup, yup
p3   = createPad(  "p3",  startXMargin2+offsetX*2, start[1],           start[0]+offsetX*3       , start[1]+offsetY  , margins2 ) # xlow, ylow, xup, yup
p4   = createPad(  "p4",  start[0],                start[1]-offsetY,   startXMargin1+offsetX    , start[1]          , margins3 ) # xlow, ylow, xup, yup
p5   = createPad(  "p5",  startXMargin1+offsetX,   start[1]-offsetY,   startXMargin2+offsetX*2  , start[1]          , margins2 ) # xlow, ylow, xup, yup
p6   = createPad(  "p6",  startXMargin2+offsetX*2, start[1]-offsetY,   start[0]+offsetX*3       , start[1]          , margins2 ) # xlow, ylow, xup, yup
p7   = createPad(  "p7",  start[0],                start[1]-offsetY*2, startXMargin1+offsetX    , start[1]-offsetY  , margins3 ) # xlow, ylow, xup, yup
p8   = createPad(  "p8",  startXMargin1+offsetX,   start[1]-offsetY*2, startXMargin2+offsetX*2  , start[1]-offsetY  , margins2 ) # xlow, ylow, xup, yup
p9   = createPad(  "p9",  startXMargin2+offsetX*2, start[1]-offsetY*2, start[0]+offsetX*3       , start[1]-offsetY  , margins2 ) # xlow, ylow, xup, yup
p10  = createPad(  "p10", start[0],                start[1]-offsetY*3, startXMargin1+offsetX    , start[1]-offsetY*2, margins3 ) # xlow, ylow, xup, yup
p11  = createPad(  "p11", startXMargin1+offsetX,   start[1]-offsetY*3, startXMargin2+offsetX*2  , start[1]-offsetY*2, margins2 ) # xlow, ylow, xup, yup
p12  = createPad(  "p12", startXMargin2+offsetX*2, start[1]-offsetY*3, start[0]+offsetX*3       , start[1]-offsetY*2, margins2 ) # xlow, ylow, xup, yup
ptotal  = createPad(  "ptotal", 0.0, 0.00, 1., 1., margins ) # xlow, ylow, xup, yup
ptotal.SetFillStyle(4000)
# p4  = createPad(  "p4", 0.00, 0.50, 0.33, 0.75, margins2 ) # xlow, ylow, xup, yup
# p5  = createPad(  "p5", 0.33, 0.50, 0.66, 0.75, margins2 ) # xlow, ylow, xup, yup
# p6  = createPad(  "p6", 0.66, 0.50, 0.99, 0.75, margins2 ) # xlow, ylow, xup, yup
# p7  = createPad(  "p7", 0.00, 0.25, 0.33, 0.50, margins2 ) # xlow, ylow, xup, yup
# p8  = createPad(  "p8", 0.33, 0.25, 0.66, 0.50, margins2 ) # xlow, ylow, xup, yup
# p9  = createPad(  "p9", 0.66, 0.25, 0.99, 0.50, margins2 ) # xlow, ylow, xup, yup
# p10 = createPad( "p10", 0.00, 0.00, 0.33, 0.25, margins2 ) # xlow, ylow, xup, yup
# p11 = createPad( "p11", 0.33, 0.00, 0.66, 0.25, margins2 ) # xlow, ylow, xup, yup
# p12 = createPad( "p12", 0.66, 0.00, 0.99, 0.25, margins2 ) # xlow, ylow, xup, yup
# p1  = createPad(  "p1", 0.00, 0.75, 0.33, 1.00, margins2 ) # xlow, ylow, xup, yup
# p2  = createPad(  "p2", 0.33, 0.75, 0.66, 1.00, margins2 ) # xlow, ylow, xup, yup
# p3  = createPad(  "p3", 0.66, 0.75, 0.99, 1.00, margins2 ) # xlow, ylow, xup, yup
# p4  = createPad(  "p4", 0.00, 0.50, 0.33, 0.75, margins2 ) # xlow, ylow, xup, yup
# p5  = createPad(  "p5", 0.33, 0.50, 0.66, 0.75, margins2 ) # xlow, ylow, xup, yup
# p6  = createPad(  "p6", 0.66, 0.50, 0.99, 0.75, margins2 ) # xlow, ylow, xup, yup
# p7  = createPad(  "p7", 0.00, 0.25, 0.33, 0.50, margins2 ) # xlow, ylow, xup, yup
# p8  = createPad(  "p8", 0.33, 0.25, 0.66, 0.50, margins2 ) # xlow, ylow, xup, yup
# p9  = createPad(  "p9", 0.66, 0.25, 0.99, 0.50, margins2 ) # xlow, ylow, xup, yup
# p10 = createPad( "p10", 0.00, 0.00, 0.33, 0.25, margins2 ) # xlow, ylow, xup, yup
# p11 = createPad( "p11", 0.33, 0.00, 0.66, 0.25, margins2 ) # xlow, ylow, xup, yup
# p12 = createPad( "p12", 0.66, 0.00, 0.99, 0.25, margins2 ) # xlow, ylow, xup, yup
pads = [ p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12 ]
# p1 = TPad("p1", "p1", 0., 0.3, 1., 1.0, 0, 0, 0)
# p1.SetMargin(0.12,0.05,0.05,0.09) #left,right,bottom,top
# p1.SetTicks(1,1)
# p1.Draw()
# p2 = TPad("p2", "p2", 0., 0.05, 1., 0.3, 0, 0, 0)
# p2.SetMargin(0.12,0.05,0.38,0.05) #left,right,bottom,top
# p2.SetTicks(1,1)
# p2.Draw()
#### draw histograms in upper pad
# p1.cd()
ptotal.cd()

for apad, theMass in enumerate(massList):
    changePad(pads[apad])
    inputGraph2sigmaName = "Limits_{0}/Option_{1}/2SigmaLimit_{0}_{1}_mass{2}_{3}".format(args.year, append, massXY, theMass)
    theGraph2sigma = inputFile.Get(inputGraph2sigmaName)
    theGraph2sigma.SetTitle("")
    theGraph2sigma.GetXaxis().SetTitle("m_{%s} [GeV]"%(othermassXY))
    theGraph2sigma.GetXaxis().SetLabelFont(42)
    theGraph2sigma.GetXaxis().SetLabelSize(0.08)
    theGraph2sigma.GetXaxis().SetTitleFont(42)
    # theGraph2sigma.GetXaxis().SetTitleSize(0.07)
    theGraph2sigma.GetXaxis().SetTitleSize(0.)
    theGraph2sigma.GetXaxis().SetTitleOffset(1.1)
    theGraph2sigma.GetXaxis().SetNdivisions(310)
    theGraph2sigma.GetXaxis().SetTickLength(0.04)
    theGraph2sigma.GetYaxis().SetLabelFont(42)
    if ((apad)%3==0): theGraph2sigma.GetYaxis().SetLabelSize(0.08)
    else: theGraph2sigma.GetYaxis().SetLabelSize(0.)
    if (apad==0):
        theGraph2sigma.GetYaxis().SetRangeUser(5e0, 5e3)
        theGraph2sigma.GetXaxis().SetRangeUser(50.,259.)
    elif (apad<3):
        theGraph2sigma.GetYaxis().SetRangeUser(5e0, 5e3)
        theGraph2sigma.GetXaxis().SetRangeUser(51.,1900.)
    else:
        theGraph2sigma.GetYaxis().SetRangeUser(5e-1,1.e3)
        theGraph2sigma.GetXaxis().SetRangeUser(50.,1900.)
    theGraph2sigma.GetYaxis().SetTitleFont(42)
    # theGraph2sigma.GetYaxis().SetTitleSize(0.07)
    theGraph2sigma.GetYaxis().SetTitleSize(0.)
    theGraph2sigma.GetYaxis().SetTitleOffset(1.1)
    # theGraph2sigma.GetYaxis().SetTitle("#sigma(pp #rightarrow X) #times BR(Y(b#bar{b}) H(b#bar{b})) [fb]")
    theGraph2sigma.GetYaxis().SetTitle("#sigma #times BR(YH) [fb]")
    theGraph2sigma.SetTitle("m_{%s} = %i GeV"%(massXY,theMass))
    theGraph2sigma.SetFillColor(color2sig)
    theGraph2sigma.SetLineWidth(0)
    theGraph2sigma.Draw("a3")

    inputGraph1sigmaName = "Limits_{0}/Option_{1}/1SigmaLimit_{0}_{1}_mass{2}_{3}".format(args.year, append, massXY, theMass)
    theGraph1sigma = inputFile.Get(inputGraph1sigmaName)
    theGraph1sigma.SetFillColor(color1sig)
    theGraph1sigma.SetLineWidth(0)
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
    print(theMass)
    print("expected")
    theGraph.Print("all")

    inputGraphName = "Limits_{0}/Option_{1}/ObservedLimit_{0}_{1}_mass{2}_{3}".format(args.year, append, massXY, theMass)
    theGraphObserved = inputFile.Get(inputGraphName)
    theGraphObserved.SetLineColor(colorObs)
    theGraphObserved.SetLineStyle(1)
    theGraphObserved.SetMarkerColor(colorObs)
    theGraphObserved.SetLineWidth(2)
    theGraphObserved.SetMarkerStyle(20)
    theGraphObserved.SetMarkerSize(0.7)
    if (args.unblind):
        theGraphObserved.Draw("same l")
        print("observed")
        theGraphObserved.Print("all")


    plotlabels = TLatex()
    plotlabels.SetTextFont(43)
    plotlabels.SetTextSize(16)
    if ((apad)%3==0):
        plotlabels.DrawLatexNDC(0.35, 0.80, "m_{{{0}}} = {1} GeV".format(massXY, theMass))
    else:
        plotlabels.DrawLatexNDC(0.2, 0.80, "m_{{{0}}} = {1} GeV".format(massXY, theMass))

ptotal.cd()


CMSlabel = TLatex()
CMSlabel.SetTextFont(63)
CMSlabel.SetTextSize( 30 )
# CMSlabel.DrawLatexNDC(0.15, 0.95, "CMS #scale[0.8]{#it{#bf{Work In Progress}}}")
CMSlabel.DrawLatexNDC(0.12, 0.95, "CMS")

if("RunII" in args.year): yearLabel="138 fb^{-1} (13 TeV)"
else: yearLabel = args.year
plotlabels.SetTextFont(43)
plotlabels.SetTextSize(20)
plotlabels.SetTextAlign(31)
plotlabels.DrawLatexNDC(0.965, 0.95, yearLabel)
plotlabels.SetTextAlign(11)

theLegend  = TLegend( 0.12,0.01,0.9,0.1 )
theLegend.SetNColumns(2);
# theLegend.AddEntry(theGraph1sigma, "Expected limit #pm1 #sigma", "f" )
# theLegend.AddEntry(theGraph2sigma, "Expected limit #pm2 #sigma", "f" )
theLegend.AddEntry(theGraph1sigma, "68% expected", "f" )
theLegend.AddEntry(theGraph2sigma, "95% expected", "f" )
theLegend.AddEntry(theGraph, "Expected 95% upper limit", "l")
if (args.unblind): theLegend.AddEntry(theGraphObserved, "Observed 95% upper limit", "l")
theLegend.SetBorderSize(0) # remove the border
theLegend.SetLineColor(0)
theLegend.SetFillColor(0)
theLegend.SetTextSize(0.028)
theLegend.SetFillStyle(0) # make the legend background transparent
theLegend.Draw("same")

theCanvas.cd()
plotlabels.SetTextFont(43)
plotlabels.SetTextSize(18)
plotlabels.SetTextAlign(31)
xpos=0.97
plotlabels.DrawLatexNDC(xpos - 0.03, 0.11, "m_{Y} [GeV]")
arrow = TArrow(0.11,0.14,xpos,0.14,0.02,"|>");
arrow.SetLineWidth(2);
arrow.Draw();
plotlabels.SetTextAngle(90.);
ypos=0.94
# plotlabels.DrawLatexNDC(0.04, ypos - 0.03, "#sigma(pp #rightarrow X) #times BR(Y(b#bar{b}) H(b#bar{b})) [fb]")
plotlabels.DrawLatexNDC(0.04, ypos - 0.03, "#sigma(pp #rightarrow X) #times BR(X #rightarrow YH #rightarrow b#bar{b}b#bar{b}) [fb]")
arrow.DrawArrow(0.06,0.19,0.06,ypos,0.02,"|>");


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

theCanvas.SaveAs(odir+"Limits{0}_allMasses.pdf".format(args.year))
del theCanvas

inputFile.Close()



