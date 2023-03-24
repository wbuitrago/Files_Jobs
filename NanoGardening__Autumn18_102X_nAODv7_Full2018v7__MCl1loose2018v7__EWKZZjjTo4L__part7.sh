#!/bin/bash
#$ -N NanoGardening__Autumn18_102X_nAODv7_Full2018v7__MCl1loose2018v7__EWKZZjjTo4L__part7
export X509_USER_PROXY=/afs/cern.ch/user/w/wbuitrag/.proxy
voms-proxy-info
export SCRAM_ARCH=slc7_amd64_gcc700
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh
cd /afs/cern.ch/user/w/wbuitrag/CMSSW_10_6_4
eval `scramv1 ru -sh`
ulimit -c 0 -s unlimited
cd $TMPDIR 
pwd 
cp /afs/cern.ch/user/w/wbuitrag/CMSSW_10_6_4/src/PhysicsTools/NanoAODTools/scripts/haddnano.py .

python /afs/cern.ch/user/w/wbuitrag/CMSSW_10_6_4/src/Jobs_cms_Davidjobsjobs//NanoGardening__Autumn18_102X_nAODv7_Full2018v7__MCl1loose2018v7/EWKZZjjTo4L/NanoGardening__Autumn18_102X_nAODv7_Full2018v7__MCl1loose2018v7__EWKZZjjTo4L__part7.py
ls -l
xrdcp -f nanoLatino_EWKZZjjTo4L__part7__MCl1loose2018v7.root root://eoscms.cern.ch//eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano//Autumn18_102X_nAODv7_Full2018v7/MCl1loose2018v7/nanoLatino_EWKZZjjTo4L__part7.root
rm nanoLatino_EWKZZjjTo4L__part7__MCl1loose2018v7.root ; rm B25E4EC1-0C76-0A4B-AB9B-30AAFFE0F49A_Skim.root
[ $? -eq 0 ] && mv /afs/cern.ch/user/w/wbuitrag/CMSSW_10_6_4/src/Jobs_cms_Davidjobsjobs//NanoGardening__Autumn18_102X_nAODv7_Full2018v7__MCl1loose2018v7/EWKZZjjTo4L/NanoGardening__Autumn18_102X_nAODv7_Full2018v7__MCl1loose2018v7__EWKZZjjTo4L__part7.jid /afs/cern.ch/user/w/wbuitrag/CMSSW_10_6_4/src/Jobs_cms_Davidjobsjobs//NanoGardening__Autumn18_102X_nAODv7_Full2018v7__MCl1loose2018v7/EWKZZjjTo4L/NanoGardening__Autumn18_102X_nAODv7_Full2018v7__MCl1loose2018v7__EWKZZjjTo4L__part7.done