#Example from NI Forum https://forums.ni.com/t5/Measurement-Studio-for-NET/FetchSpectrum-Using-Python-and-RFmx/m-p/3182954#M17056
import clr
import sys
import time

# location of assemblies
assy_path = r'C:\Program Files (x86)\National Instruments\MeasurementStudioVS2010\DotNET\Assemblies\Current'
sys.path.append(assy_path)

clr.AddReference("NationalInstruments.RFmx.SpecAnMX.Fx40")
clr.AddReference("NationalInstruments.RFmx.InstrMX.Fx40")
clr.AddReference("NationalInstruments.Common")

from NationalInstruments.RFmx.InstrMX import *
from NationalInstruments.RFmx.SpecAnMX import *
import NationalInstruments
import System

# VSA Settings
resourceName = 'VST1'

#Init session
instrSession = RFmxInstrMX(resourceName, '')

#Configure Spectrum type acquisition
specAn = RFmxSpecAnMXExtension.GetSpecAnSignalConfiguration(instrSession)
specAn.SelectMeasurements('',RFmxSpecAnMXMeasurementTypes.Spectrum,True)
specAn.Commit('')

# execute acquisition
specAn.Initiate('','')


# create variable name before passing it to .NET method
spectrum = NationalInstruments.Spectrum[System.Single](0)
_,spectrum = specAn.Spectrum.Results.FetchSpectrum('',10,spectrum)
#spectrumData=spectrum.GetRawData()
print 'Spectrum size: {0}'.format(spectrum.SampleCount)

#Close instrument session
instrSession.Close()