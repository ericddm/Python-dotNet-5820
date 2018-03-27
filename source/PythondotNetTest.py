import clr
import sys
import time
import os

# Location of assemblies
dotNetFWDirectory = r"C:\Program Files (x86)\IVI Foundation\IVI\Microsoft.NET\Framework32"

assy_path = os.path.join(dotNetFWDirectory, r'v4.0.30319\NationalInstruments.ModularInstruments.NIRfsa 17.1.0')

print(assy_path)

sys.path.append(assy_path)

clr.AddReference("NationalInstruments.ModularInstruments.NIRfsa.Fx40")
clr.AddReference("NationalInstruments.Common")

#Import .NET drivers
import NationalInstruments
import System

from NationalInstruments import *
from NationalInstruments.ModularInstruments.NIRfsa import *
from NationalInstruments import PrecisionTimeSpan
