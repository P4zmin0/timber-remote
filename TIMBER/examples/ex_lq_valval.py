from TIMBER.Analyzer import *
from TIMBER.Tools.Common import *

import ROOT
import sys, os

from TIMBER.Tools.RestFramesHandler import load_restframes

sys.path.append('../../')
sys.path.append('../../../')

num_threads = 1
file_name = 'root://cmsxrootd.fnal.gov//store/mc/RunIISummer20UL18NanoAODv9/TprimeTprime_M-1500_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/40000/447AD74F-034B-FA42-AD05-CD476A98C43D.root'

handler_name = 'rename_me.cc'
class_name = 'LQ_VALVAL_RestFrames_Container'

# Enable using 4 threads
ROOT.ROOT.EnableImplicitMT(num_threads)

# load rest frames handler
load_restframes(num_threads, handler_name, class_name, 'rfc')

# Create analyzer instance
a = analyzer(file_name)

print('==========================INITIALIZED ANALYZER========================')

myCuts = CutGroup('myCuts')
myCuts.Add('njet',        'nJet>3') # need to ensure four jets exist
myCuts.Add('ntau',        'nTau>1') # need 2 taus

rframeVars = VarGroup('restFrameVars')
rframeVars.Add('VF_mass', 'rfc.compute_mass(rdfslot_, Tau_pt, Tau_eta, Tau_phi, Tau_mass, Jet_pt, Jet_eta, Jet_phi, Jet_mass)')
rframeVars.Add('VF_mass_1', 'VF_mass[0]')
rframeVars.Add('VF_mass_2', 'VF_mass[1]')
rframeVars.Add('VF_mass_ratio', 'VF_mass_1/VF_mass_2')
rframeVars.Add('VF_mass_avg', '(VF_mass_1+VF_mass_2)*0.5')

nodeToPlot = a.Apply([myCuts, rframeVars])

myHist1 = a.GetActiveNode().DataFrame.Histo1D(('m_a', 'Mass of first of the particles', 25, 10, 510), 'VF_mass_1')
myHist2 = a.GetActiveNode().DataFrame.Histo1D(('m_b', 'Mass of second of the particles', 25, 10, 510), 'VF_mass_2')
myHist3 = a.GetActiveNode().DataFrame.Histo1D(('m_a/m_b', 'Mass ratio of the two particles', 25, 0, 2), 'VF_mass_ratio')
myHist4 = a.GetActiveNode().DataFrame.Histo1D(('m_avg', 'Mass average of the two', 25, 10, 510), 'VF_mass_avg')

out = ROOT.TFile.Open('test_lq_valval_out.root','UPDATE')
myHist1.Write()
myHist2.Write()
myHist3.Write()
myHist4.Write()
out.Close()

a.PrintNodeTree('test_lq_valval_out.png')

