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

referenceLevel =  0.00                     # /* dBm */
externalAttenuation = 0.00                # /* dB */
frequencySource = RFmxInstrMXConstants.OnboardClock
frequency = 10.0e+6                       # /* Hz */
timeout = 10

# Measurement Settings
averagingCount = 10
averagingEnabled = RFmxSpecAnMXSpurAveragingEnabled.False
averagingType = RFmxSpecAnMXSpurAveragingType.Rms

NumberOfRanges = 1
NumberOfSpursToReport = 5

averagingCount = 1
averagingEnabled = RFmxSpecAnMXSpurAveragingEnabled.False
averagingType = RFmxSpecAnMXSpurAveragingType.Rms

rangeEnabled = [RFmxSpecAnMXSpurRangeEnabled.True]
startFrequency = [999e+6]            # /* Hz */
stopFrequency = [1001e+6]              # /* Hz */

rbwFilterType = [RFmxSpecAnMXSpurRbwFilterType.Gaussian]
rbwFilterAutoBandwidth = [RFmxSpecAnMXSpurRbwAutoBandwidth.True]
rbwFilterBandwidth = [30e+3]         #  /* Hz */

vbwAuto = [RFmxSpecAnMXSpurRangeVbwFilterAutoBandwidth.True]
vbw = [30.0e3]                       # /* Hz */
vbwToRbwRatio = [3]

detectorType = [RFmxSpecAnMXSpurRangeDetectorType.None]
detectorPoints = [1001]

absoluteLimitMode = [RFmxSpecAnMXSpurAbsoluteLimitMode.Couple]
absoluteLimitStart = [0 ] # Max of searched amplitude range
absoluteLimitStop = [-10.00]

peakThreshold = [-50] #Threshold above which we look for spurs
peakExcursion = [5]   #Minimum power abouve threashold to report as a spur

numberOfSpursToReport = [5]

traceRangeIndex = 0

#Create Result variables
spurFrequency = [0] 
spurAmplitude = [0]
spurMargin = [0]
spurAbsLimit = [0]
spurRangeIndex = [0]



#Initialize instrument session
instrSession = RFmxInstrMX(resourceName, '')
#Initialize SpecAn personality handle
specAn = RFmxSpecAnMXExtension.GetSpecAnSignalConfiguration(instrSession)

#Configure Instrument settings
instrSession.ConfigureFrequencyReference("", frequencySource, frequency)
specAn.ConfigureReferenceLevel("", referenceLevel)
specAn.ConfigureExternalAttenuation("", externalAttenuation)

#Configure Spur measurement type acquisition
specAn.SelectMeasurements('',RFmxSpecAnMXMeasurementTypes.Spur,True)

specAn.Spur.Configuration.ConfigureAveraging("", averagingEnabled, averagingCount, averagingType)
specAn.Spur.Configuration.ConfigureNumberOfRanges("", NumberOfRanges)
specAn.Spur.Configuration.ConfigureRangeFrequencyArray("", startFrequency, stopFrequency, rangeEnabled)
specAn.Spur.Configuration.ConfigureRangeRbwArray("", rbwFilterAutoBandwidth, rbwFilterBandwidth, rbwFilterType)
specAn.Spur.Configuration.ConfigureRangeAbsoluteLimitArray("", absoluteLimitMode, absoluteLimitStart,  absoluteLimitStop)
specAn.Spur.Configuration.ConfigureRangeNumberOfSpursToReportArray("", numberOfSpursToReport)
specAn.Spur.Configuration.ConfigureRangePeakCriteriaArray("", peakThreshold, peakExcursion)
specAn.Spur.Configuration.ConfigureRangeDetectorArray("", detectorType, detectorPoints)
specAn.Spur.Configuration.ConfigureRangeVbwFilterArray("", vbwAuto, vbw, vbwToRbwRatio)
specAn.Spur.Configuration.ConfigureTraceRangeIndex("", traceRangeIndex)


specAn.Commit('')

# execute Measurement
specAn.Initiate('','')

#Retrieve result list
_, spurFrequency, spurAmplitude, spurMargin, spurAbsLimit, spurRangeIndex = specAn.Spur.Results.FetchAllSpurs("", timeout, spurFrequency, spurAmplitude, spurMargin, spurAbsLimit, spurRangeIndex )


#Print Results
print 'Spur 1'
print 'Spur Frequencies:  {0}'.format(spurFrequency[0])
print 'Spur Amplitude:  {0}'.format(spurAmplitude[0])

print 'Spur 2'
print 'Spur Frequencies:  {0}'.format(spurFrequency[1])
print 'Spur Amplitude:  {0}'.format(spurAmplitude[1])

print 'Spur 3'
print 'Spur Frequencies:  {0}'.format(spurFrequency[2])
print 'Spur Amplitude:  {0}'.format(spurAmplitude[2])

print 'Spur 4'
print 'Spur Frequencies:  {0}'.format(spurFrequency[3])
print 'Spur Amplitude:  {0}'.format(spurAmplitude[3])

print 'Spur 5'
print 'Spur Frequencies:  {0}'.format(spurFrequency[4])
print 'Spur Amplitude:  {0}'.format(spurAmplitude[4])





#Close instrument session
instrSession.Close()