import ALP4 as alp4
import numpy as np

def InitiateMasterMode(version="4.2", libDir=r"G:\ALP-4.2\ALP-4.2 high-speed API"):
    """Initiate a session in the DMD.

    Args:
        -> version (str, optional): version of the ALP4 controller. Defaults to "4.2".
        -> libDir (regexp, optional): Directory of the required .dll files of the ALP4 module. Defaults to r"G:\ALP-4.2\ALP-4.2 high-speed API".

    Returns:
        DMD: DMD session (class)
    """
    DMD = alp4.ALP4(version = version, libDir = libDir)
    
    DMD.Initialize()  # Initialize the device

    DMD.ProjControl(alp4.ALP_PROJ_MODE, alp4.ALP_MASTER) #Put DMD on master mode
    DMD.DevControl(alp4.ALP_SYNCH_POLARITY, alp4.ALP_LEVEL_HIGH) #Change polarity of synch signal

    return DMD

def CheckParameters(operate):
    def Check(masks,
              DMD,
              pictureTime,
              illuminationTime,
              synchPulseWidth,
              synchDelay,
              ):
        msg = ""
        
        if np.any(masks<0.) or np.any(masks>1.):
            msg = msg + "-> Pixel values of masks must be in the interval [0,1].\n"
            
        if msg!="":
            print(msg)
            return None
        
        return operate(masks,
                       DMD,
                       pictureTime,
                       illuminationTime,
                       synchPulseWidth,
                       synchDelay,
                       )
        
    return Check

@CheckParameters
def AllocateMasks(masks,
                  DMD,
                  pictureTime,
                  illuminationTime,
                  synchPulseWidth=100,
                  synchDelay=0,
                  ):
    """Allocates the masks in the DMD memory under the sequence name 'sequence'.

    Args:
        masks (_type_): masks to be stored in the DMD memory with shape (nsamples, 768, 1024)
        DMD (_type_): Initiated DMD class.
        pictureTime (_type_): Time dedicated for individual masks
        illuminationTime (_type_): Time the mask is kept on the DMD screen which must be inferior than the pictureTime.
        synchPulseWidth (int, optional): Time length of the trigger signal sent from the DMD to the camera. Defaults to 100.
        synchDelay (int, optional): Delay between the start of the picture time and the illumination time. Defaults to 0.
    Returns:
        class: DMD object with the masks allocated in the internal memory.
    """
    DMD.sequence = DMD.SeqAlloc(nbImg=masks.shape[0], bitDepth=1)
    
    DMD.Nmasks = masks.shape[0]
    
    DMD.SeqPut(imgData=255*masks.ravel(),
               SequenceId=DMD.sequence)
    
    DMD.SetTiming(SequenceId=DMD.sequence, 
                  pictureTime = pictureTime, 
                  illuminationTime = illuminationTime,
                  synchPulseWidth = synchPulseWidth,
                  synchDelay = synchDelay,
                  triggerInDelay = 0)
    
    return DMD