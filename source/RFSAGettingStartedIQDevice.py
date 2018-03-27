import clr
import sys
import time
import os

# Location of assemblies
dotNetFWDirectory = r"C:\Program Files (x86)\IVI Foundation\IVI\Microsoft.NET\Framework32"
dotNetClassLibrary = r'v4.0.30319\NationalInstruments.ModularInstruments.NIRfsa 17.1.0'
assy_path = os.path.join(dotNetFWDirectory, dotNetClassLibrary)
print(".NET Library: " + dotNetClassLibrary)

sys.path.append(assy_path)

clr.AddReference("NationalInstruments.ModularInstruments.NIRfsa.Fx40")
clr.AddReference("NationalInstruments.Common")

# Import .NET drivers
import NationalInstruments
#import System

from NationalInstruments import *
from NationalInstruments.ModularInstruments.NIRfsa import *
from NationalInstruments import PrecisionTimeSpan

# Instrument Settings
ResourceName = 'PXI1Slot2' # Instrument alias in MAX
IQinVerticalRange = 0.5 # Vpp
IQinCarrierFrequency = 0.0 # FPGA DSP Frequencyshift
IQinRate = 1e6 # Samples per second
SamplesperRecord = 2048
RefClockSource = 'PXI_CLK'

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

#print("IQ In Vertical Range: " + str(instrSession.Configuration.Vertical.))

# Close Instrument
instrSession.Close()
