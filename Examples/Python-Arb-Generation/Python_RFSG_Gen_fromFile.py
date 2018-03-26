import ctypes
from ctypes import*
from nptdms import TdmsFile

NIRFSG_VAL_CW = 1000
NIRFSG_VAL_ARB_WAVEFORM  = 1001
NIRFSG_VAL_SCRIPT = 1002

NIRFSG_ATTR_IQ_RATE = 1250452
NIRFSG_ATTR_ARB_PRE_FILTER_GAIN =  1150025

 
def niRFSG_init(
        resource_name, id_query, reset):

    session = ctypes.c_ulong()

    global cfunc

    cfunc = ctypes.windll.LoadLibrary("c:\\Program Files (x86)\\IVI Foundation\\IVI\\Bin\\niRFSG.dll")

    error_code = cfunc.niRFSG_init(ctypes.c_char_p(resource_name.encode('ascii')), ctypes.c_bool(id_query), ctypes.c_bool(reset), ctypes.byref(session))

    return session, error_code

def niRFSG_GetError(
        session, error_code):

    error_buffer = ctypes.create_string_buffer(2048)

    error = ctypes.c_int32()

    ret = cfunc.niRFSG_GetError(session, ctypes.byref(error), ctypes.c_uint(2048),  error_buffer)

    return  error_buffer.value

def niRFSG_ConfigureRF(
        session, frequency, power):

    error_code = cfunc.niRFSG_ConfigureRF(session, ctypes.c_double(frequency), ctypes.c_double(power))

    return  error_code

def niRFSG_ConfigureGenerationMode(
        session, mode):

    error_code = cfunc.niRFSG_ConfigureGenerationMode(session, ctypes.c_int32(mode))

    return  error_code

def niRFSG_SetAttributeViReal64(
            session, channel, attribute_id, attribute_value):

        error_code = cfunc.niRFSG_SetAttributeViReal64(session, ctypes.c_char_p(channel.encode('ascii')), ctypes.c_int32(attribute_id), ctypes.c_double(attribute_value))

        return error_code

def niRFSG_GetAttributeViReal64(
            session, channel, attribute_id):

        attribute_value = ctypes.c_double()

        error_code = cfunc.niRFSG_GetAttributeViReal64(session, ctypes.c_char_p(channel.encode('ascii')), ctypes.c_int32(attribute_id), ctypes.byref(attribute_value))

        return error_code, attribute_value.value


def niRFSG_ConfigureSignalBandwidth(
        session, bandwidth ):
    error_code = cfunc.niRFSG_ConfigureSignalBandwidth(session, ctypes.c_double(bandwidth))

    return error_code

def niRFSG_WriteArbWaveform(
            session, waveform_name , number_of_samples, i_data, q_data, more_data_pending):

        idata =(ctypes.c_double*number_of_samples)(*i_data)
        qdata =(ctypes.c_double*number_of_samples)(*q_data)

        error_code = cfunc.niRFSG_WriteArbWaveform(session, ctypes.c_char_p(waveform_name.encode('ascii')),
                                                       ctypes.c_int32(number_of_samples), idata, qdata, ctypes.c_bool(more_data_pending))

        return error_code

def niRFSG_Initiate(
            session):
        error_code = cfunc.niRFSG_Initiate(session)

        return error_code

def niRFSG_CheckGenerationStatus(
        session):

    is_done = ctypes.c_bool()
    error_code = cfunc.niRFSG_CheckGenerationStatus(session, ctypes.byref(is_done))

    return error_code, is_done.value

def niRFSG_ConfigureOutputEnabled(
        session, output_enabled):

    error_code = cfunc.niRFSG_CheckGenerationStatus(session, ctypes.c_bool(output_enabled))

    return error_code

def niRFSG_close(
        session):

    error_code = cfunc.niRFSG_close(session)

    return error_code

if __name__ == "__main__":
    # execute only if run as a script

#    tdms_file = TdmsFile("c:\\temp\\ni80211ag_20MHz.tdms")
    tdms_file = TdmsFile("C:\\Users\\aes\\Desktop\\Algo\\Text-based automation\\Python Example Arb Generation\\Bluetooth_DH1_example.tdms")
    print(tdms_file.groups())
    print(tdms_file.group_channels(tdms_file.groups()[0]))

    # Use this with signals saved from Wlan SFP
#    channel = tdms_file.object('waveforms', 'channel0')

    # Use this with signals saved from BT SFP

    channel = tdms_file.object('waveforms', 'niBT SG Waveform')

    data = channel.data

    data_rate = channel.property('NI_RF_IQRate')

    data_i = data [0::2]
    data_q = data [1::2]

    print ("IQ data rate: ", data_rate)
    #print ("I = ", data_i)
    #print ("Q = ", data_q)


    #Initialize instrument session
    session, error_code = niRFSG_init("VST1", 1, 1)
    if (error_code!=0): print (niRFSG_GetError(session, error_code))

    #Configure generation parameters
    error_code = niRFSG_ConfigureRF(session, 1000E6, -20.0)
    if (error_code!=0): print (niRFSG_GetError(session, error_code))

    error_code = niRFSG_ConfigureGenerationMode(session, NIRFSG_VAL_ARB_WAVEFORM)
    if (error_code!=0): print (niRFSG_GetError(session, error_code))

    error_code = niRFSG_SetAttributeViReal64(session, "", NIRFSG_ATTR_ARB_PRE_FILTER_GAIN, -1.0)
    if (error_code!=0): print (niRFSG_GetError(session, error_code))

    error_code = niRFSG_SetAttributeViReal64(session, "", NIRFSG_ATTR_IQ_RATE, data_rate)
    if (error_code!=0): print (niRFSG_GetError(session, error_code))

    error_code, iq_rate = niRFSG_GetAttributeViReal64(session, "", NIRFSG_ATTR_IQ_RATE)
    if (error_code!=0): print (niRFSG_GetError(session, error_code))

    #print ("Configured IQ rate = ", iq_rate)

    error_code = niRFSG_ConfigureSignalBandwidth(session, 0.4*data_rate)
    if (error_code != 0): print(niRFSG_GetError(session, error_code))

    error_code = niRFSG_WriteArbWaveform(session, "", len(data_i), data_i, data_q, False)
    if (error_code!=0): print (niRFSG_GetError(session, error_code))

    error_code = niRFSG_Initiate(session)
    if (error_code!=0): print (niRFSG_GetError(session, error_code))
    
    raw_input("\nPress Enter to stop generation...")

    error_code = niRFSG_ConfigureOutputEnabled(session, False)
    if (error_code!=0): print (niRFSG_GetError(session, error_code))

    error_code = niRFSG_close(session)
    if (error_code!=0): print (niRFSG_GetError(session, error_code))