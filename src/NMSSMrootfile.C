// reading a text file
#include <iostream>
#include <fstream>
#include <string>
#include "TFile.h"
#include "TGraph.h"
#include "TTree.h"
#include "TCut.h"
#include "TString.h"
using namespace std;

void saveGraph(TTree *t, TString cut){

    int n = t->Draw("mY:limit",cut,"goff");
    TGraph *g = new TGraph(n,t->GetV1(),t->GetV2());
    TString saveName=cut.ReplaceAll("=","");
    saveName=saveName.ReplaceAll("<","");
    saveName=saveName.ReplaceAll("410","400");
    g->Write(saveName);

}

int main () {
    string line;

    // TFile* ofile = TFile::Open("input/NMSSMdata.root", "RECREATE");
    // auto g = new TGraph2D("input/NMSSMdata.txt");
    // auto g = new TGraph2D();
    TFile f("input/NMSSMdata.root","recreate");
    TTree *t = new TTree("t", "tree from .csv");
    t->ReadFile("input/NMSSMdata.csv", "mX/I:mY/I:limit/D");
    saveGraph(t, "mX<410");
    saveGraph(t, "mX==500");
    saveGraph(t, "mX==600");
    saveGraph(t, "mX==700");
    saveGraph(t, "mX==800");
    saveGraph(t, "mX==900");
    saveGraph(t, "mX==1000");
    // saveGraph(t, "mX==1100");
    saveGraph(t, "mX==1200");
    saveGraph(t, "mX==1400");
    saveGraph(t, "mX==1600");
    // int n = t->Draw("mY:limit","mX==500","goff");
    // TGraph *g = new TGraph(n,t->GetV1(),t->GetV2());
    // g->Print("all");
    // t->Draw("mY");

    // ifstream myfile ("input/NMSSMdata.txt");
    // if (myfile.is_open())
    // {

    //     // while(getline(myfile, line)) {
    //         // cout << line << endl;
    //     // }
    //     while (getline(myfile, ID, ',')) {
    //         cout << "ID: " << ID << " " ;

    //         getline(myfile, nome, ',') ;
    //         cout << "User: " << nome << " " ;

    //         getline(myfile, idade, ',') ;
    //         cout << "Idade: " << idade << " "  ;

    //         getline(myfile, genero);
    //         cout << "Sexo: " <<  genero<< " "  ;
    //     }
    //     myfile.close();
    // }

    // else cout << "Unable to open file";

    // g->Print("all");

    return 0;
}
