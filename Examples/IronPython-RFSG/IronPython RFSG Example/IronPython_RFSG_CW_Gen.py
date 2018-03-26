# This example generates a CW and waits for user input to stop generation

import clr
import sys
import time

# location of assemblies
assy_path = r'C:\Program Files (x86)\IVI Foundation\IVI\Microsoft.NET\Framework32\v4.0.30319\NationalInstruments.ModularInstruments.NIRfsg 17.1.0'
sys.path.append(assy_path)

clr.AddReference("NationalInstruments.ModularInstruments.NIRfsg.Fx40")
clr.AddReference("NationalInstruments.Common")

#Import .NET drivers
from NationalInstruments import *
from NationalInstruments.ModularInstruments.NIRfsg import *
from System import *

# VSA Settings
resourceName = 'VST1'
freq = 1000000000
power = -10

#Print settings to display
print "Resource name: " + resourceName
print "Frequency: " + str(freq)
print "Power: " + str(power)

#Initialize Instrument Session
print("Initializing RFSG session")
instrSession = NIRfsg(resourceName, True, True)

#Configure RF Settings
instrSession.RF.Configure(freq, power)

#Begin Generation
instrSession.Initiate()

#Wait for User Input to stop generation
raw_input("Press Enter to stop generation...")

#Disable output and close instrument session
instrSession.RF.OutputEnabled = False;
instrSession.Close()