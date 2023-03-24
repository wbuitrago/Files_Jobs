#!/usr/bin/env python 
import os, sys 
import subprocess
import shutil
import ROOT 
ROOT.PyConfig.IgnoreCommandLineOptions = True 
 
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor 
from LatinoAnalysis.NanoGardener.modules.Dummy import *
import LatinoAnalysis.Tools.userConfig as userConfig
 
from LatinoAnalysis.NanoGardener.modules.LeptonMaker import *
from LatinoAnalysis.NanoGardener.modules.LeptonSel import *
from LatinoAnalysis.NanoGardener.modules.JetSel import *
from LatinoAnalysis.NanoGardener.modules.FatJetCorrHelper import *
from LatinoAnalysis.NanoGardener.modules.FatJetMaker import *
from LatinoAnalysis.NanoGardener.modules.PromptParticlesGenVarsProducer import *
from LatinoAnalysis.NanoGardener.modules.GenVarProducer import *
from LatinoAnalysis.NanoGardener.modules.GenLeptonMatchProducer import *
from LatinoAnalysis.NanoGardener.modules.HiggsGenVarsProducer import *
from LatinoAnalysis.NanoGardener.modules.TopGenVarsProducer import *
from LatinoAnalysis.NanoGardener.modules.wwNLLcorrectionWeightProducer import *
from LatinoAnalysis.NanoGardener.modules.WGammaStar import *
from LatinoAnalysis.NanoGardener.modules.GGHUncertaintyProducer import *
from LatinoAnalysis.NanoGardener.modules.QQHUncertaintyProducer import *
from LatinoAnalysis.NanoGardener.modules.DressedLeptonProducer import *
from LatinoAnalysis.NanoGardener.modules.EFTReweighter import *
 
leptonMaker = lambda : LeptonMaker()
leptonSel = lambda : LeptonSel("Full2018v7", "Loose", 1)
jetSel = lambda : JetSel(2,"custom",15.0,4.7,"CleanJet")
corr_fatjet_mc = createFatjetCorrector( globalTag="Regrouped_Autumn18_V19_MC", dataYear="2018", jetType="AK8PFPuppi", isMC=True, redojec=True, applySmearing=True)
fatjetMaker = lambda : FatJetMaker(jetid=0, minpt=200, maxeta=2.4, max_tau21=0.45, mass_range=[40, 250], over_lepR=0.8, over_jetR=0.8)
PromptParticlesGenVars = lambda : PromptParticlesGenVarsProducer()
GenVar = lambda : GenVarProducer()
GenLeptonMatch = lambda : GenLeptonMatchProducer()
HiggsGenVars = lambda : HiggsGenVarsProducer()
TopGenVars = lambda : TopGenVarsProducer()
wwNLL = lambda : wwNLLcorrectionWeightProducer()
wGS = lambda : WGammaStarV2()
ggHUncertaintyProducer = lambda : GGHUncertaintyProducer()
qqHUncertaintyProducer = lambda : QQHUncertaintyProducer()
dressedLeptons = lambda : DressedLeptonProducer(0.3)
EFTGen = lambda : EFTReweighter("EWKZZjjTo4L")
 
sourceFiles=[
    "root://xrootd-cms.infn.it//store/mc/RunIIAutumn18NanoAODv7/ZZJJTo4L_EWK_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/60000/23C72D32-B220-6846-AE03-9A8DDFA64790.root"
]

files=[]

for source in sourceFiles:
    fname = os.path.basename(source).replace(".root", "_input.root")
    for att in range(5):
        if source.startswith("root://"):
            proc = subprocess.Popen(["xrdcp", "-f", source, "./" + fname])
            proc.communicate()
            if proc.returncode == 0:
                out, err = subprocess.Popen(["xrdfs", source[:source.find("/", 7)], "stat", source[source.find("/", 7) + 1:]], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                try:
                    size = int(out.split("\n")[2].split()[1])
                except:
                    if hasattr(userConfig, "postProcSkipSizeValidation") and userConfig.postProcSkipSizeValidation:
                        sys.stderr.write("Failed to obtain original file size but skipping validation as requested by user\n")
                        break
                    raise
            else:
                continue
        else:
            shutil.copyfile(source, "./" + fname)
            size = os.stat(source).st_size

        try:
            if os.stat(os.path.basename(fname)).st_size == size:
                break
        except:
            try:
                os.unlink(os.path.basename(fname))
            except:
                pass
    else:
        raise RuntimeError("Failed to download " + source)

    files.append(fname)

p = PostProcessor(  "."   ,          
                    files ,          
                    cut="((nElectron+nMuon)>0)" ,       
                    branchsel=None , 
                    outputbranchsel=None , 
                    modules=[        
                          leptonMaker(),
                          leptonSel(),
                          jetSel(),
                          corr_fatjet_mc(),
                          fatjetMaker(),
                          PromptParticlesGenVars(),
                          GenVar(),
                          GenLeptonMatch(),
                          HiggsGenVars(),
                          wGS(),
                          dressedLeptons(),
                            ],      
                    provenance=True, 
                    fwkJobReport=False, 
                    haddFileName="nanoLatino_EWKZZjjTo4L__part2__MCl1loose2018v7.root", 
                 ) 
 
p.run() 
 
for fname in files:
    try:
        os.unlink(fname)
        os.rename(fname.replace("_input.root", "_input_Skim.root"), fname.replace("_input.root", "_Skim.root"))
    except:
        pass
