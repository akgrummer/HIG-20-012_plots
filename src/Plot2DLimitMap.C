#include "Riostream.h"
#include "TFile.h"
#include "TH2D.h"
#include "TLine.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TLatex.h"
#include "TROOT.h"
#include "TGraphAsymmErrors.h"
#include <stdlib.h>
#include <map>
#include <tuple>
#include <vector>
#include <fstream>
#include <algorithm>
#include <stdio.h>


// g++  -std=c++17 -I `root-config --incdir`  -o Plot2DLimitMap Plot2DLimitMap.cc `root-config --libs` -O3

std::vector<float> getBinning(const std::vector<float>& listOfPoints)
{
    uint numberOfPoints = listOfPoints.size();
    std::vector<float> binning(numberOfPoints+1);
    for (int point=0; point<numberOfPoints-1; ++point) binning[point+1] = (listOfPoints[point]+listOfPoints[point+1])/2.;
    binning[0]              = 2.*listOfPoints[0] - binning[1];
    binning[numberOfPoints] = 2.*listOfPoints[numberOfPoints-1] - binning[numberOfPoints-1];
    for(auto bin : binning) std::cout << bin << " - ";
    std::cout<<std::endl;
    return binning;
}

std::vector<float> doubleBinning(const std::vector<float>& originalBinning)
{
    uint originalNumberOfPoints = originalBinning.size();
    uint numberOfPoints = originalNumberOfPoints*2-1;
    std::vector<float> binning(numberOfPoints);
    binning[0] = originalBinning[0];
    binning[numberOfPoints-1] = originalBinning[originalNumberOfPoints-1];
    for(uint point=1; point<originalNumberOfPoints-1; ++point) binning[point*2] = originalBinning[point];
    for(uint point=0; point<originalNumberOfPoints-1; ++point) binning[point*2+1] = (originalBinning[point]+originalBinning[point+1])/2.;
    // for(auto bin : binning) std::cout << bin << " - ";
    // std::cout<<std::endl;
    return binning;
}

std::vector<std::string> splitByLine(const std::string& inputFileName)
{
    std::vector<std::string> fileNameList;
    std::ifstream fList (inputFileName);
    if (!fList.good())
    {
        std::cerr << "*** Sample::openFileAndTree : ERROR : could not open file " << inputFileName << std::endl;
        abort();
    }
    std::string line;
    while (std::getline(fList, line))
    {
        line = line.substr(0, line.find("#", 0)); // remove comments introduced by #
        while (line.find(" ") != std::string::npos) line = line.erase(line.find(" "), 1); // remove white spaces
        while (line.find("\n") != std::string::npos) line = line.erase(line.find("\n"), 1); // remove new line characters
        while (line.find("\r") != std::string::npos) line = line.erase(line.find("\r"), 1); // remove carriage return characters
        if (!line.empty()) fileNameList.emplace_back(line);
    }
    return fileNameList;
}

std::pair<float, float> getMassesFromSignalName(const std::string& signalName)
{

    std::string mXbeginString = "sig_NMSSM_bbbb_MX_"      ;
    std::string mXendString   = "_MY_" ;
    std::string mYbeginString = "_MY_"      ;
    std::string mYendString   = "\0"   ;

    int mXbegin = signalName.find(mXbeginString) + mXbeginString.size();
    int mXend   = signalName.find(mXendString);
    int mYbegin = signalName.find(mYbeginString) + mYbeginString.size();
    int mYend   = signalName.find(mYendString);
    int xMass = atoi(signalName.substr(mXbegin, mXend-mXbegin).c_str());
    int yMass = atoi(signalName.substr(mYbegin, mYend-mYbegin).c_str());

    return std::make_pair(xMass, yMass);
}

void Plot2DLimitMap(TString tag, std::string year, std::string option = "syst", std::string obsORexp="Central")
{
    gROOT->SetBatch(true);

    std::string histogramName = "Limits_" + year + "/Option_" + option + "/LimitMap"+obsORexp+"_" + year + "_" + option;
    TString inputFileName = "hists/Limits_"+tag+".root";
    auto *inputFile = new TFile(inputFileName);
    if(inputFile == nullptr)
    {
        std::cout<< "File " << inputFileName << " does not exist, aborting..." << std::endl;
        abort();
    }
    TH2D* limitMap = (TH2D*)inputFile->Get(histogramName.c_str());
    if(limitMap == nullptr)
    {
        std::cout<< "Histogram " << histogramName << " does not exist, aborting..." << std::endl;
        abort();
    }
    limitMap->SetDirectory(0);

    std::string canvasName = "CentralLimitMap_" + year + "_" + option;
    TCanvas* theCanvas = new TCanvas(canvasName.c_str(), canvasName.c_str(), 800, 800);
    gPad->SetTickx(1);
    gPad->SetTicky(1);
    // gPad->SetMargin(0.12,0.16,0.12,0.09);
    limitMap->Draw("colz");

    std::string plotTitle = "Central Limit " + year;
    limitMap->SetTitle(plotTitle.c_str());
    limitMap->GetXaxis()->SetTitle("m_{Xreco} [GeV]");
    limitMap->GetXaxis()->SetLabelFont(62);
    limitMap->GetXaxis()->SetLabelSize(0.045);
    limitMap->GetXaxis()->SetTitleFont(62);
    limitMap->GetXaxis()->SetTitleSize(0.045);
    limitMap->GetYaxis()->SetTitle("m_{Yreco} [GeV]");
    limitMap->GetYaxis()->SetLabelFont(62);
    limitMap->GetYaxis()->SetLabelSize(0.045);
    limitMap->GetYaxis()->SetTitleFont(62);
    limitMap->GetYaxis()->SetTitleSize(0.045);
    limitMap->GetYaxis()->SetTitleOffset(1.8);
    limitMap->GetZaxis()->SetTitleOffset(1.3);
    limitMap->GetZaxis()->SetLabelFont(62);
    limitMap->GetZaxis()->SetLabelSize(0.035);
    limitMap->GetZaxis()->SetTitleFont(62);
    limitMap->GetZaxis()->SetTitleSize(0.045);
    limitMap->SetMinimum(1.);
    // limitMap->SetMaximum(2000.);
    limitMap->SetMaximum(900.);
    limitMap->SetStats(false);
    theCanvas->SetLogz();
    // theCanvas->SetLogy();

    // theCanvas->SaveAs("results/"+tag.c_str()+"/"+(std::string(theCanvas->GetName()) + ".pdf").c_str());
    // theCanvas->SaveAs("results/Limits_"+tag+"/"+theCanvas->GetName() + ".pdf");
    // theCanvas->SaveAs("results/Limits_"+tag+"/"+theCanvas->GetName() + ".png");
    // theCanvas->SaveAs("results/"+tag.c_str()+"/"+std::string(theCanvas->GetName()) + ".png").c_str());
    // theCanvas->SaveAs((std::string(theCanvas->GetName()) + "_log.png").c_str());


    if(year == "RunII" && option == "syst")
    {
        std::vector<std::string> signalList = splitByLine("input/listOfSamples.txt");

        std::vector<float> xMassList;
        std::vector<float> yMassList;

        for(const auto& signal : signalList)
        {
            const auto xAndYmass = getMassesFromSignalName(signal);
            if(std::find (xMassList.begin(), xMassList.end(), xAndYmass.first ) == xMassList.end()) xMassList.emplace_back(xAndYmass.first );
            if(std::find (yMassList.begin(), yMassList.end(), xAndYmass.second) == yMassList.end()) yMassList.emplace_back(xAndYmass.second);
        }

        std::sort(xMassList.begin(), xMassList.end());
        std::sort(yMassList.begin(), yMassList.end());

        auto xOriginalBinning = getBinning(xMassList);
        auto yOriginalBinning = getBinning(yMassList);

        // auto xBinning = doubleBinning(xOriginalBinning);
        // auto yBinning = doubleBinning(yOriginalBinning);
        // std::cout<<"Doing custom binning though"<<std::endl;

        // xOriginalBinning.clear();
        // yOriginalBinning.clear();
        // binning before mx=650 with different mY values added
        //                       350, 450, 550, 650, 750, 850, 950, 1050, 1150, 1300, 1500, 1700
        // xOriginalBinning.assign({ 350, 450, 550, 625, 675, 750, 850, 950, 1050, 1150, 1300, 1500, 1700 });
        //                        55, 65, 75, 85, 95, 112.5, 137.5, 175, 225, 275, 350, 450, 550, 650, 750, 850, 950, 1100, 1300, 1500
        // yOriginalBinning.assign({55, 65, 75, 85, 95, 112.5, 137.5, 175, 225, 275, 350, 450, 550, 650, 750, 850, 950, 1100, 1300, 1500});

        std::string theoryCanvasName = obsORexp+"LimitMap_RunII_TheoryComparison";
        TCanvas* theTheoryCanvas = new TCanvas(theoryCanvasName.c_str(), theoryCanvasName.c_str(), 800, 800);
        gPad->SetTickx(1);
        gPad->SetTicky(1);
        gPad->SetMargin(0.16,0.20,0.12,0.05);

        limitMap->SetTitle("");
        limitMap->Draw("colz");

        /* std::string inputTheoryFileName = "/uscms/home/fravera/nobackup/DiHiggs_v1/CMSSW_10_2_5/src/bbbbAnalysis/HXSG_NMSSM_recommendations_00.root"; */
        /* std::string inputTheoryFileName = "/uscms/home/fravera/nobackup/DiHiggs_v1/CMSSW_10_2_5/src/bbbbAnalysis/HXSG_NMSSM_recommendations_00.root"; */
        std::string inputTheoryFileName = "input/HXSG_NMSSM_recommendations_00.root";
        std::string inputTheoryPlotName = "g_bbbb";

        TFile inputTheoryFile(inputTheoryFileName.c_str());
        TGraphAsymmErrors* theTheoryGraph = (TGraphAsymmErrors*)inputTheoryFile.Get(inputTheoryPlotName.c_str());

        // TH2D *theoryContour = new TH2D("theoryContour", "theoryContour", xBinning.size()-1, xBinning.data(), yBinning.size()-1, yBinning.data());
        TH2D *theoryContour = new TH2D("theoryContour", "theoryContour", xOriginalBinning.size()-1, xOriginalBinning.data(), yOriginalBinning.size()-1, yOriginalBinning.data());

        double contours[4];
        contours[0] = 1000.;

        for(int xBin = 1; xBin<=theoryContour->GetNbinsX(); ++xBin)
        {
            float xBinCenter = theoryContour->GetXaxis()->GetBinCenter(xBin);
            if(xBinCenter<400. || xBinCenter>1000.) continue;
            if (xBinCenter==587.50)xBinCenter=600.0;
            float theoreticalXsec = theTheoryGraph->Eval(xBinCenter) * 1000.;
            for(int yBin = 1; yBin<=theoryContour->GetNbinsY(); ++yBin)
            {
                float yBinCenter = theoryContour->GetYaxis()->GetBinCenter(yBin);
                float limit = limitMap->GetBinContent(limitMap->GetXaxis()->FindBin(xBinCenter), limitMap->GetYaxis()->FindBin(yBinCenter));
                if(limit>0 && limit <= theoreticalXsec)
                {
                    theoryContour->SetBinContent(xBin, yBin, 1000.);
                    // std::cout<<"MX: "<<xBinCenter<<" MY:"<<yBinCenter<< " theory: "<< theoreticalXsec<<" exp: "<<limit<<std::endl;
                    printf ("MX: %8.2f MX: %8.2f theory: %8.2f limit: %8.2f \n", xBinCenter, yBinCenter, theoreticalXsec, limit);

                }
            }
        }

        Double_t x1{0.}, x2{0.}, y1{0.}, y2{0.};
        TLine *cont_line = new TLine(x1,y1,x2,y2);
        cont_line->SetLineWidth(4);
        cont_line->SetLineColor(kRed);
        for(int xBin = 1; xBin<=theoryContour->GetNbinsX(); ++xBin){
            float xBinCenter = theoryContour->GetXaxis()->GetBinCenter(xBin);
            if(xBinCenter<400. || xBinCenter>1000.) continue;
            float prevY{0.};
            float currY{0.};
            //Int_t maxYbin{0};
            for(int yBin = 1; yBin<=theoryContour->GetNbinsY(); ++yBin){
                    currY = theoryContour->GetBinContent(xBin, yBin);
                    if (currY<prevY){
                      x1 = theoryContour->GetXaxis()->GetBinLowEdge(xBin);
                      x2 = theoryContour->GetXaxis()->GetBinUpEdge(xBin);
                      y1 = theoryContour->GetYaxis()->GetBinLowEdge(yBin);
                      y2 = theoryContour->GetYaxis()->GetBinLowEdge(yBin);
                      cont_line->DrawLine(x1, y1, x2, y2);
                      }

                    if (currY>prevY){
                      x1 = theoryContour->GetXaxis()->GetBinLowEdge(xBin);
                      x2 = theoryContour->GetXaxis()->GetBinUpEdge(xBin);
                      y1 = theoryContour->GetYaxis()->GetBinLowEdge(yBin);
                      y2 = theoryContour->GetYaxis()->GetBinLowEdge(yBin);
                      if (yBin!=1) cont_line->DrawLine(x1, y1, x2, y2);
                      }
                    prevY=currY;
            }
        }

        for(int yBin = 1; yBin<=theoryContour->GetNbinsY(); ++yBin){
            float prevX{0.};
            float currX{0.};
            //Int_t maxYbin{0};
            for(int xBin = 1; xBin<=theoryContour->GetNbinsX(); ++xBin){
                    float xBinCenter = theoryContour->GetXaxis()->GetBinCenter(xBin);
                    if(xBinCenter<400. || xBinCenter>1000.) continue;
                    currX = theoryContour->GetBinContent(xBin, yBin);
                    if (currX<prevX){
                      x1 = theoryContour->GetXaxis()->GetBinLowEdge(xBin);
                      x2 = theoryContour->GetXaxis()->GetBinLowEdge(xBin);
                      y1 = theoryContour->GetYaxis()->GetBinUpEdge(yBin);
                      y2 = theoryContour->GetYaxis()->GetBinLowEdge(yBin);
                      cont_line->DrawLine(x1, y1, x2, y2);
                      }

                    if (currX>prevX){
                      x1 = theoryContour->GetXaxis()->GetBinLowEdge(xBin);
                      x2 = theoryContour->GetXaxis()->GetBinLowEdge(xBin);
                      y1 = theoryContour->GetYaxis()->GetBinLowEdge(yBin);
                      y2 = theoryContour->GetYaxis()->GetBinUpEdge(yBin);
                      if (xBin!=1) cont_line->DrawLine(x1, y1, x2, y2);
                      }
                    prevX=currX;
            }
        }


        theoryContour->SetContour(1, contours);
        theoryContour->SetFillStyle(3357);
        theoryContour->SetLineColor(kRed+2);
        theoryContour->SetLineWidth(2);
        theoryContour->SetFillColor(kRed+2);

        theoryContour->Draw("box same");
        theTheoryCanvas->SetLogz();
        auto CMSlabel = new TLatex();
        CMSlabel->SetTextFont(63);
        CMSlabel->SetTextSize( 30 );
        CMSlabel->DrawLatexNDC(0.16, 0.96, "CMS #scale[0.8]{#it{#bf{Work In Progress}}}");

        
        auto legend = new TLegend(0.2,0.83,0.52,0.93);
        legend->AddEntry(theoryContour,"#splitline{Limit below maximally allowed values}{in NMSSM, given by LHC Higgs WG}","f");
        legend->SetBorderSize(0);
        legend->SetLineColor(0);
        legend->SetFillColor(0);
        legend->SetTextSize(0.028);
        legend->SetFillStyle(0);
        legend->Draw();
        // theTheoryCanvas->SetLogy();
        // theTheoryCanvas->SetLogy();
        TString SaveName = Form("results/d%s.pdf",theTheoryCanvas->GetName());
        theTheoryCanvas->SaveAs(SaveName);
         // theTheoryCanvas->SaveAs((std::string(theTheoryCanvas->GetName()) + "_log.png").c_str());


    }

    gROOT->SetBatch(false);

    delete inputFile;
    return;
}

int main(int argc, char** argv)
{

    if(argc!=2)
    {
        std::cout<<"Usage: ./Plot2DLimitMap <tag>"<<std::endl;
        exit(EXIT_FAILURE);
    }

    TString inputTag=argv[1];

    // std::vector<std::string> optionList {"statOnly", "syst"};
    // std::vector<std::string> yearList {"2016", "2017", "2018", "RunII"};
    std::vector<std::string> optionList {"syst"};
    std::vector<std::string> yearList {"RunII"};
    std::vector<std::string> obsORexpList {"Central", "Observed"};

    // std::vector<std::string> optionList {"syst"};
    //std::vector<std::string> yearList {"RunII"};

    for(const auto & year : yearList)
    {
        for(const auto & option : optionList)
        {
            for(const auto & obsORexp : obsORexpList)
            {
                Plot2DLimitMap(inputTag, year, option, obsORexp);
            }
        }
    }

    return 0;

}
