import clr
import sys
import time
import os
import argparse

import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()

parser.add_argument('--resource')

args = parser.parse_args()

# Location of assemblies
dotNetFWDirectory = r"C:\Program Files (x86)\IVI Foundation\IVI\Microsoft.NET\Framework32"
dotNetClassLibrary = r'v4.0.30319\NationalInstruments.ModularInstruments.NIRfsa 17.1.0'
assy_path = os.path.join(dotNetFWDirectory, dotNetClassLibrary)
print(".NET Library: " + dotNetClassLibrary)

sys.path.append(assy_path)

clr.AddReference("NationalInstruments.ModularInstruments.NIRfsa.Fx40")
clr.AddReference("NationalInstruments.Common")

# Import .NET drivers
#import NationalInstruments
#import System

from NationalInstruments.ModularInstruments.NIRfsa import *
from NationalInstruments import PrecisionTimeSpan
from NationalInstruments import ComplexDouble

# Instrument Settings
ResourceName = args.resource # Instrument alias in MAX
IQinVerticalRange = 0.5 # Vpp
IQinCarrierFrequency = 0.0 # FPGA DSP Frequencyshift
IQinRate = 10e6 # Samples per second
SamplesPerRecord = 2048

# Initialize Instrument
instrSession = NIRfsa(ResourceName, True, True)

# Configure Instrument
print("Reference Clock Source: " + instrSession.Configuration.ReferenceClock.Source.ToString())
instrSession.Configuration.ReferenceClock.Configure(RfsaReferenceClockSource.PxiClock, 10e6)
print("Reference Clock Source: " + instrSession.Configuration.ReferenceClock.Source.ToString())

print("Acquisition Type: " + str(instrSession.Configuration.AcquisitionType))
instrSession.Configuration.AcquisitionType = RfsaAcquisitionType.IQ
print("Acquisition Type: " + str(instrSession.Configuration.AcquisitionType))

print("IQ In Input Port: " + str(instrSession.Configuration.SignalPath.Advanced.InputPort))
instrSession.Configuration.SignalPath.Advanced.InputPort = RfsaInputPort.IQIn
print("IQ In Input Port: " + str(instrSession.Configuration.SignalPath.Advanced.InputPort))

print("IQ In Carrier Frequency: " + str(instrSession.Configuration.IQInPortChannels.CarrierFrequency))
instrSession.Configuration.IQInPortChannels.CarrierFrequency = IQinCarrierFrequency
print("IQ In Carrier Frequency: " + str(instrSession.Configuration.IQInPortChannels.CarrierFrequency))

print("IQ In Rate: " + str(instrSession.Configuration.IQ.IQRate))
instrSession.Configuration.IQ.IQRate = IQinRate
print("IQ In Rate: " + str(instrSession.Configuration.IQ.IQRate))

instrSession.Configuration.IQ.NumberOfRecordsIsFinite = True
print("Number of record is finite: " + str(instrSession.Configuration.IQ.NumberOfRecordsIsFinite))

instrSession.Configuration.IQ.NumberOfSamples = SamplesPerRecord
print("Number of Samples per Record: " + str(instrSession.Configuration.IQ.NumberOfSamples))

# Begin Acquisition and read data     
timeout = PrecisionTimeSpan(10.0)
nicomplexdoublearray = instrSession.Acquisition.IQ.ReadIQSingleRecordComplex(timeout)

print("NIComplexDoubleArray Type: " + str(type(nicomplexdoublearray)))
print("NIComplexDoubleArray[0]: "+ str(nicomplexdoublearray[0]))
print("NIComplexDouble.[0]Real Type: "+ str(type(nicomplexdoublearray[0].Real)))
print("NIComplexDouble[0].Real: " +str(nicomplexdoublearray[0].Real))

iTemp = []
qTemp = []
_, iTemp, qTemp = ComplexDouble.DecomposeArray(nicomplexdoublearray, iTemp, qTemp)

iData = []
qData = []
for complexdouble in nicomplexdoublearray:
    iData.append(complexdouble.Real)
    qData.append(complexdouble.Imaginary)

fig = plt.figure()

ax0 = fig.add_subplot(2,1,1)
ax0.plot(iData)

ax1 = fig.add_subplot(2,1,2)
ax1.plot(qData)

plt.show()

# Close Instrument
instrSession.Close()
