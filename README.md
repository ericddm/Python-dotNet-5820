## PXIe-5820 Python .NET Example

This examples shows how to setup a system and run very basics RF examples from Python. The
approach are two approaches: calling the CLR (Common Language Runtime) to directly iterface
with .NET classes and creating wrappers around the driver c dll using cpython.

### Setting up Enviroment

- Install [Python](https://www.python.org/downloads/) 3.6.4
	- Version of Python is tied to Python .NET, pick your version according to their support
	- Install launcher for all users
	- Add Python 3.6 to PATH
	- Customization (pip, Documentation, IDLE, Test Suite, py launcher)
	- Everything else left as default (03-26-2018)

- Install NI-RFSA .NET Support
	- [National Instruments .NET Support](http://www.ni.com/product-documentation/14434/en/)
	- [RFSA](http://www.ni.com/download/ni-rfsa-17.1/6894/en/) be patient it is a big download
	- [.NET RFSA](http://www.ni.com/download/ni-rfsa-.net-class-library-17.1/6909/en/)

- Instal pythonnet
	- [Installation Wiki](https://github.com/pythonnet/pythonnet/wiki/Installation)
	'pip install pythonnet'

- Install .NET Framework 4.6.1
	- [.NET Framework 4.6.1](https://www.microsoft.com/en-us/download/details.aspx?id=49981)

- Install Matplotlib (optional to run demo examples)
	- python -m pip install -U pip setuptools
	- python -m pip install matplotlib
	- python -m pip install numpy

- Maybe you do need the .NET Core 2.1.101 SDK (leaving it last to ensure it is in fact needed)

### Testing the Envirotment
- Run \source\PythondoNetTest.py
	This examples simply import the clr and rfsa .NET libraries.

### RFSA Getting StartedIQDevice.py
This python script was created based on the RFSA exampled called: "RFSA Getting Started IQ (IQ Device).vi"

### Documentation
- C:\Program Files (x86)\IVI Foundation\IVI\Microsoft.NET\Framework32\v4.0.30319\NationalInstruments.ModularInstruments.NIRfsa 17.1.0\NINETRfsaFx40Ref.chm
- http://zone.ni.com/reference/en-XX/help/375857A-01/html/allmembers_t_nationalinstruments_complexdouble/
- https://stackoverflow.com/questions/19600315/how-to-use-a-net-method-which-modifies-in-place-in-python
- http://ironpython.net/documentation/dotnet/dotnet.html#methods-with-ref-or-out-parameters
- https://stackoverflow.com/questions/16484167/python-net-framework-reference-argument-double
