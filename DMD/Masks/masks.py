import numpy as np

def CircleMask(r = 50, shape=(1024, 768)):
    canvas = np.zeros((1, *shape))
    x_mid, y_mid = int((shape[0]/2)), int((shape[1]/2))

    # create the circle
    circ = np.zeros((2*r,2*r))

    x = np.arange(2*r) - int((r-1))

    xx = np.array(np.meshgrid(x,x))
    xx = np.sum(xx**2, axis=0)

    circ[np.where(xx<=r**2)] = 1.

    # place circle on mask 
    if r%2==0:
        canvas[0, x_mid-int(r):x_mid+int(r), y_mid-int(r):y_mid+int(r)] = circ
    else:
        canvas[0, x_mid-int(r):x_mid+int(r), y_mid-int(r):y_mid+int(r)] = circ

    canvas = np.swapaxes(canvas, axis1=1, axis2=2)

    return canvas