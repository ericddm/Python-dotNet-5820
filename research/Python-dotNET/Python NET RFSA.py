# Simple IQ aquisition

import clr
import sys
import time

# location of assemblies
assy_path = r'C:\Program Files (x86)\IVI Foundation\IVI\Microsoft.NET\Framework32\v4.0.30319\NationalInstruments.ModularInstruments.NIRfsa 17.1.0'
sys.path.append(assy_path)

clr.AddReference("NationalInstruments.ModularInstruments.NIRfsa.Fx40")
clr.AddReference("NationalInstruments.Common")

#Import .NET drivers
import NationalInstruments
import System
from NationalInstruments import *
from NationalInstruments.ModularInstruments.NIRfsa import *
from NationalInstruments import PrecisionTimeSpan

# VSA Settings
resourceName = 'VST1'
freq = 1000000000 # 1GHz
power = -10
samples = 10000 # 10 k Samples
IQRate = 100000000 # 100 MSamples/sec

# ##Print settings to display
print "Resource name: " + resourceName
print "Frequency: " + str(freq)
print "Power: " + str(power)

#Loop for performance test
start = time.clock()

for x in range (0,20):
    #Initialize Instrument Session
    #print("Initializing RFSA session")
    instrSession = NIRfsa(resourceName, True, True)

    #Configure RF Settings
    instrSession.Configuration.AcquisitionType = RfsaAcquisitionType.IQ
    instrSession.Configuration.Vertical.ReferenceLevel = power
    instrSession.Configuration.IQ.CarrierFrequency = freq
    instrSession.Configuration.IQ.NumberOfSamples = samples
    instrSession.Configuration.IQ.NumberOfSamplesIsFinite = True
    instrSession.Configuration.IQ.IQRate = IQRate
   
    #raw_input("Press Enter to begin generation...")

    #Begin Acquisition and read data 
    timeout = PrecisionTimeSpan(10.0)
    result = instrSession.Acquisition.IQ.ReadIQSingleRecordComplex(timeout)

    #Disable output and close instrument session
    instrSession.Close()

stop = time.clock()

print "execution time:"
print stop - start
