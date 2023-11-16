from pypylon import pylon
from collections import Counter
import time
import numpy as np


class BaslerController:

    tlFactory = pylon.TlFactory.GetInstance()
    devices = tlFactory.EnumerateDevices()
    cameras = pylon.InstantCameraArray(len(devices))
    device_types = []
    device_names = []
    for i, cam in enumerate(cameras):
        cam.Attach(tlFactory.CreateDevice(devices[i]))
        device_type = cam.GetDeviceInfo().GetModelName()
        device_types.append(device_type)
        device_names.append(device_type)
    device_types = dict(Counter(device_types))
    for device_type, n in device_types.items():
        if n < 2:
            continue

        count = 0
        while True:
            try:
                index = device_names.index(device_type)
                device_names[index] = "%s:%d" % (device_type, count)
                count += 1
            except:
                break

    def __init__(self):

        pass

    def open(self, camera_no=0, exposure_time=100, gain=0.0, num_buffers=12,
             grab_latest=True):

        self.camera = self.cameras[camera_no]
        self.camera.Attach(self.tlFactory.CreateDevice(self.devices[camera_no]))
        self.camera.Open()
        self.camera.ExposureAuto.SetValue('Off')
        self.camera.ExposureTime.SetValue(exposure_time)
        self.camera.GainAuto.SetValue('Off')
        self.camera.Gain.SetValue(gain)
        self.camera.MaxNumBuffer = num_buffers
        self._grab_latest = grab_latest

    def close(self):
        if self.camera is not None:
            self.stop_grabbing()
            self.camera.Close()
        self.camera = None

    @property
    def width(self):
        return self.camera.SensorWidth

    @property
    def height(self):
        return self.camera.SensorHeight

    @property
    def exposure_time(self):
        return self.camera.ExposureTime

    @exposure_time.setter
    def exposure_time(self, value: int):
        self.camera.ExposureTime.SetValue(value)

    @property
    def gain(self):
        return self.camera.Gain

    @gain.setter
    def gain(self, value: float):
        self.camera.Gain.SetValue(value)

    @property
    def grab_latest(self):
        return self._grab_latest

    @grab_latest.setter
    def grab_latest(self, value: bool):
        self._grab_latest = value

    def start_grabbing(self):
        if not self.camera.IsGrabbing():
            strategy = pylon.GrabStrategy_LatestImageOnly if self._grab_latest \
                else pylon.GrabStrategy_OneByOne
            self.camera.StartGrabbing(strategy)

    def stop_grabbing(self):
        if self.camera.IsGrabbing():
            self.camera.StopGrabbing()

    def grab(self):
        if not self.camera.IsGrabbing():
            self.start_grabbing()
        grab_result = \
            self.camera.RetrieveResult(500, pylon.TimeoutHandling_ThrowException)

        result = grab_result.Array if grab_result.GrabSucceeded() else None
        grab_result.Release()
        return result


class SimulateBaslerController(BaslerController):

    _width = 100
    _height = 200

    def __init__(self):
        BaslerController.__init__(self)
        self.grid_x = np.empty([self._width, self._height])
        for x in range(self._width):
            self.grid_x[x,:] = x / self._width
        self.grid_y = np.empty([self._width, self._height])
        for y in range(self._height):
            self.grid_y[:,y] = y / self._height
        self._gain = 0
        self._exposure_time = 10
        self._mean_x = 0.5
        self._mean_y = 0.5
        self._rms_x = 0.05
        self._rms_y = 0.05
        self._beam_width = 0.05
        self._beam_height = 0.05
        # parameters for random walk
#        self._d2 =
#        self._gamma =
#        self._sigma = np.sqrt(2.0 * self._gamma * kB * temperature / mass))
#        self._dt =
#        self._sdt = np.sqrt(self._dt)


    def open(self, camera_no=0, exposure_time=100, gain=0.0, num_buffers=12,
             grab_latest=True):
        pass

    def close(self):
        pass

    def width(self):
        return self._width

    def height(self):
        return self._height

    @property
    def exposure_time(self):
        return self._exposure_time

    @exposure_time.setter
    def exposure_time(self, value: int):
        self._exposure_time = value

    @property
    def gain(self):
        return self._gain

    @gain.setter
    def gain(self, value: float):
        self._gain = value

    @property
    def beam_width(self):
        return self._beam_width

    @beam_width.setter
    def beam_width(self, val):
        self._beam_width = val

    @property
    def beam_height(self):
        return self._beam_height

    @beam_height.setter
    def beam_height(self, val):
        self._beam_height = val

    @property
    def mean_x(self):
        return self._mean_x

    @mean_x.setter
    def mean_x(self, val):
        self._mean_x = val

    @property
    def mean_y(self):
        return self._mean_y

    @mean_y.setter
    def mean_y(self, val):
        self._mean_y = val

    @property
    def rms_x(self):
        return self._rms_x

    @rms_x.setter
    def rms_x(self, val):
        self._rms_x = val

    @property
    def rms_y(self):
        return self._rms_y

    @rms_y.setter
    def rms_y(self, val):
        self._rms_y = val

    def start_grabbing(self):
        pass

    def stop_grabbing(self):
        pass

    def grab(self):
#        import pdb
#        pdb.set_trace()
        pos_x = np.random.normal(self._mean_x, self._rms_x)
        pos_y = np.random.normal(self._mean_y, self._rms_y)
        data = np.exp(-((self.grid_x - pos_x)/self._beam_width)**2) \
            * np.exp(-((self.grid_y - pos_y)/self._beam_height)**2)
        return data

        dWx = np.random.normal(0, sdt);
        dWy = np.random.normal(0, sdt);
        self._vx += \
            - self._dt * (self._gamma * self._vx \
                         + self._d2 * (self._x - self._mean_x)) \
            + self._sigma * dWx
        self._x += self._vx * self._dt;
        self._vy += \
            - self._dt * (self._gamma * self._vy \
                          + self._d2 * (self._y - self._mean_y)) \
            + self._sigma * dWy
        self._y += self._vy * self._dt;
