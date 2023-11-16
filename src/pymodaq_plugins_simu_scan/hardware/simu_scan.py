import numpy as np

class SimuScanController:

    axes_names = ['X', 'Y']
    _width = 200
    _height = 200
    cam_names = ['CAM1']
#    _pos_x = _width / 2
#    _pos_y = _height / 2

    def __init__(self):
        self._pos_x = self._width / 2
        self._pos_y = self._height / 2
        self._beam_width = 0.05 * self._width
        self._beam_height = 0.05 * self._height
        self.grid_x = np.empty([self._width, self._height])
        for x in range(self._width):
            self.grid_x[:,x] = x
        self.grid_y = np.empty([self._width, self._height])
        for y in range(self._height):
            self.grid_y[y,:] = y

    def pos(self, axis_name):
        if axis_name == 'X':
            return self._pos_x
#            return SimuScanController._pos_x
        if axis_name == 'Y':
            return self._pos_y
#            return SimuScanController._pos_y
        return None

    def move(self, axis_name, pos):
        if axis_name == 'X':
            self._pos_x = pos
#            SimuScanController._pos_x = pos
        if axis_name == 'Y':
            self._pos_y = pos
#            SimuScanController._pos_y = pos

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def grab(self):
        #pos_x = self._width / 2  # np.random.normal(self._pos_x, self._rms_x)
        #pos_y = self._height / 2 # np.random.normal(self._pos_y, self._rms_y)
#        data = np.exp(-((self.grid_x - SimuScanController._pos_x) \
#                        / self._beam_width)**2) \
#            * np.exp(-((self.grid_y - SimuScanController._pos_y) \
#                       / self._beam_height)**2)
        data = np.exp(-((self.grid_x - self._pos_x) / self._beam_width)**2) \
            * np.exp(-((self.grid_y - self._pos_y) / self._beam_height)**2)
        return data
