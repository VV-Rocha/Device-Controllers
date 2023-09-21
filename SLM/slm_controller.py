import numpy as np
from holoeye import slmdisplaysdk

class SLM_state():
    """
    Object storing the state of the spatial light modulator (SLM).
    """
    ## {"model": ((width, height), (physical width (mm), physical height (mm)))}
    global types_list
    types_list = [np.int8, np.int32, np.int64, np.float32, np.float64]

    global database
    database = {"LCR2500": ((1024, 768), (19.5, 14.6)),
                "PLUTO":((1920, 1080),(15.36, 8.64)),
                "PLUTO_AMP":((1920, 1080),(15.36, 8.64)),
                "DMD_DLP":((1024, 768),(1024*10.8e-6/1e-3, 768*10.8e-6/1e-3)),
                "LC2012":((1024, 768),(1024*36e-3, 768*36e-3)),
                }
    
    def __init__(self,
                 model="LCR2500",
                 reference=(0, 0),
                 monitor_number=0,
                 bit_depth=8,
                 inversion=(1, 1),
                 ):
        """Initiate the SLM state variables.

        Args:
            model (str, optional): Model of the SLM to be controlled allowing to load the devices properties. Defaults to "LCR2500".
            reference (tuple, optional): Shift reference point of the mask to placed on the SLM device. Defaults to (0, 0).
            monitor_number (int, optional): Monitor number associated with the SLM device. Defaults to 0.
            bit_depth (int, optional): Bit depth of the SLM intensity (2**bit_depth - 1 possible values). Defaults to 8.
            inversion (tuple, optional): Inversion of the mask on the SLM device. Possible values are 1 for no inversion and -1 inversion.. Defaults to (1, 1).

        Returns:
            _type_: None
        """
        
        try:
            self.SLM_px, self.SLM_mm = SLMSpecsDatabase(model)
            self.monitor_number = monitor_number
            self.reference = (0, 0)
            self.UpdateReference((int(self.SLM_px[0]/2) + reference[0],
                               int(self.SLM_px[1]/2) + reference[1]))
            self.bit_depth = bit_depth
            self.max_value = 2**bit_depth - 1
            self.UpdateInversion(inversion)
            self.BlankMask()

        except Exception:
            return None

    def CheckMask(operate):
        def Verification(self, mask):
            types_list = [np.int16, np.int32, np.int64, np.int8, np.float16, np.float32, np.float64]
            
            msg = ""
            if mask.dtype not in types_list:
                msg = msg + f"-> The mask values are of invalid type. Valid dtypes are {types_list}.\n"
            elif mask.shape != self.SLM_px:
                msg = msg + f"-> The new mask has size {mask.shape} and the required is {self.SLM_px}\n"
            if msg!="":
                print(msg)
                return None
            
            return operate(self, mask)
        return Verification

    @CheckMask
    def UpdateMask(self, mask):
        """Change the mask state of the SLM.

        Args:
            -> mask (array): Mask of the SLM screen with shape (1024, 768)
        """
        self.mask = mask

    def BlankMask(self, dtype=np.float64):
        """
        Changes the mask to zeros.
        """
        self.mask =  np.zeros(self.SLM_px, dtype=dtype)

    def InFrame(function):
        def CheckBoundaries(self, dshift):
            if int(dshift[0])!=dshift[0] or int(dshift[1])!=dshift[1]:
                print("-> Shift values in tuple must be of type int.\n")
                return None
            if (self.reference[0]+dshift[0] > int(self.SLM_px[0])) or (self.reference[0]+dshift[0] <= 0) or (self.reference[1]+dshift[1] > int(self.SLM_px[1])) or (self.reference[1]+dshift[1] <= 0):
                print("-> New center reference is outside SLM boundaries.")
                return None
            return function(self, dshift)

        return CheckBoundaries

    @InFrame
    def UpdateReference(self, dshift):
        """
        Update the shift of the center of the mask on the SLM.
        
        Parameters:
            -> dshift - Tuple (int, int) to update the shift state.
        """
        self.reference = (self.reference[0]+dshift[0], self.reference[1]+dshift[1])

    def ValidInversion(function):
        def CheckValues(self, inversion):
            valid_values = [-1,1]
            if inversion[0] not in valid_values or inversion[1] not in valid_values:
                print(f"-> Inversion values are not valid. Valid values are {valid_values}.\n")
                return None
            return function(self, inversion)
            
        return CheckValues

    @ValidInversion
    def UpdateInversion(self, inversion):
        """
        Update the inversion constant of the mask on the SLM.
        
        Args:
            -> inversion (int): Inversion of the mask on the SLM device. Possible values are 1 for no inversion and -1 inversion.
        """
        self.inversion = inversion
        
def ModelInDatabase(operate):
    def inner(model):
        if model in database.keys():
            return operate(model)
        else:
            print(f"-> This model is not present in our current database of SLMs.\n")
            print(f"-> Consider contributing with the model {model} specifications to our database.\n")
            return None
    return inner

@ModelInDatabase
def SLMSpecsDatabase(model):
    """Extracts the parameters of the SLM if it is registered in the database.

    Args:
        -> model (str): string with the model of the SLM.

    Returns:
        SLM_px: tuple with the width and height number of pixels
        SLM_mm: tuple with the width and height in milimeters
    """
    SLM_px, SLM_mm = database[model]
    return SLM_px, SLM_mm




class SLM_API():
    """
    This class works as an API between the SLM state object and the SLM device.
    """
    def __init__(self, slm_state=None):
        if isinstance(slm_state, SLM_state):
            self.slm_state = slm_state
        elif type(slm_state) is str:
            self.slm_state = SLM_state(slm_state)
        else:
            print(f"-> The input SLM state is of invalid type. Please input the SLM_state object type or a string type with the valid model.\n")
        
        self.slm = slmdisplaysdk.SLMInstance()
        
        mask = slmdisplaysdk.createFieldSingle(*self.slm_state.SLM_px) ## allocation of memory to store mask

    """ Erase if the current version of the class if working.
    def __init__(self, slm_state=None, model=None):
        ## Verification of slm_state object compatibility or alternatively use the 
        if isinstance(slm_state, SLM_state):
            self.slm_state = slm_state
        elif slm_state is None:
            if not model is None:
                slm_state = SLM_state(model)
            else:
                print(f"-> Both the SLM state and the model parameters are missing. Please insert a valid input for either of the parameters.\n")
        elif not isinstance(slm_state, SLM_state) and slm_state is not None:
            print(f"-> The input slm state class seems to be invalid. Please use a valid object.")
            return None
        
        self.slm = slmdisplaysdk.SLMInstance()
        
        mask = slmdisplaysdk.createFieldSingle(*self.slm_state.SLM_px) ## allocation of memory to store mask
    """
    
    def Open(self):
        self.slm.open()
        self.slm.showData(self.slm_state.mask[::self.slm_state.inversion[0], ::self.slm_state.inversion[1]])
        print(f"-> SLM is active with the state mask.\n")
        
    def Close(self):
        self.slm.close()
        self.slm.utilsWaitUntilClosed()
        print(f"-> SLM is closed.\n")
        
    def UpdateMask(self, mask):
        try:
            self.slm_state.UpdateMask(mask)
            self.slm.showData(mask)
        except:
            print(f"-> Mask is invalid.\n")
            return None
        