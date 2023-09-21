from ximea import xiapi

def ConfigCamera(cam, exposure=2000):
    cam.set_exposure(exposure)

    cam.set_gpi_mode("XI_GPI_TRIGGER")
    cam.set_trigger_source("XI_TRG_EDGE_RISING")
    cam.set_trigger_selector("XI_TRG_SEL_FRAME_START")

    cam.set_downsampling_type("XI_SKIPPING")
    cam.set_downsampling("XI_DWN_2x2")
    cam.set_gain(0)
    cam.set_imgdataformat("XI_MONO8")

    print("Image width:", cam.get_width())
    print("Image height:", cam.get_height())
    print("Image offsetX:", cam.get_offsetX())
    print("Image offsetY:", cam.get_offsetY())

    cam.set_buffers_queue_size(cam.get_buffers_queue_size_maximum())

    cam.set_counter_selector("XI_CNT_SEL_API_SKIPPED_FRAMES")
    
    return cam

def InitiateCamera(exposure=2000):
    cam = xiapi.Camera()
    cam.open_device()
    
    cam = ConfigCamera(cam, exposure)  # Initiate default configs
    
    return cam