from pymodaq.utils.daq_utils import ThreadCommand
from pymodaq.utils.data import DataFromPlugins, Axis, DataToExport
from pymodaq.control_modules.viewer_utility_classes import DAQ_Viewer_base, \
    comon_parameters, main
from pymodaq.utils.parameter import Parameter
import numpy as np

from pymodaq_plugins_simu_scan.hardware.simu_scan import SimuScanController


class DAQ_2DViewer_simu_scan(DAQ_Viewer_base):
    """ Instrument plugin class for a simulated camera 2D viewer.
    
    This object inherits all functionalities to communicate with PyMoDAQ’s
    DAQ_Viewer module through inheritance via DAQ_Viewer_base. It makes a
    bridge between the DAQ_Viewer module and the Python wrapper of a
    particular instrument.

    TODO Complete the docstring of your plugin with:
        * The set of instruments that should be compatible with this
          instrument plugin.
        * With which instrument it has actually been tested.
        * The version of PyMoDAQ during the test.
        * The version of the operating system.
        * Installation instructions: what manufacturer’s drivers should
          be installed to make it run?

    Attributes:
    -----------
    controller: object
        The particular object that allow the communication with the
        hardware, in general a python wrapper around the hardware library.
         
    # TODO add your particular attributes here if any

    """

    params = comon_parameters + [
      {'title': 'Device name:', 'name': 'device_name', 'type': 'str',
         'limits': SimuScanController.cam_names,
       'value': SimuScanController.cam_names[0] \
       if len(SimuScanController.cam_names) > 0 else ''},
    ]

    def ini_attributes(self):
        self.controller: BaslerController = None
        self.x_axis = None
        self.y_axis = None

    def ini_detector(self, controller=None):
        """Detector communication initialization

        Parameters
        ----------
        controller: (object)
            custom object of a PyMoDAQ plugin (Slave case). None if 
            only one actuator/detector by controller (Master case)

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True
        """
        new_controller=SimuScanController()
        self.ini_detector_init(old_controller=controller,
                               new_controller=new_controller)

        device_name = self.settings['device_name']
        device_number = self.controller.cam_names.index(device_name) \
            if device_name != '' else 0

        #self.controller.open(device_number)

        self.image_size = [self.controller.width, self.controller.height]
        data_x_axis = np.linspace(0, self.controller.width,
                                  self.controller.width)
        self.x_axis = Axis(data=data_x_axis, label='x', units='pixel', index=1)
        data_y_axis = np.linspace(0, self.controller.height,
                                  self.controller.height)
        self.y_axis = Axis(data=data_y_axis, label='y', units='pixel', index=0)

        data = [np.zeros(self.image_size)]
        data_out = [DataFromPlugins(name='basler', data=data, dim='Data2D',
                                    labels=['image'],
                                    axes=[self.x_axis, self.y_axis]), ]
        self.dte_signal_temp.emit(DataToExport('simu_cam', data=data_out))

        info = "Simulation camera initialised"
        initialized = True
        return info, initialized

    def close(self):
        pass

    def commit_settings(self, param: Parameter):
        """Apply the consequences of a change of value in the detector settings

        Parameters
        ----------
        param: Parameter
            A given parameter (within detector_settings) whose value has 
            been changed by the user
        """
        #if param.name() == "exposure_time":
        #    self.controller.exposure_time = \
        #        self.settings.child('exposure_time').value()
        pass

    def grab_data(self, Naverage=1, **kwargs):
        """Start a grab from the detector

        Parameters
        ----------
        Naverage: int
            Number of hardware averaging (if hardware averaging is possible,
            self.hardware_averaging should be set to True in class preamble
            and you should code this implementation)
        kwargs: dict
            others optionals arguments
        """
        self.callback()

    def callback(self):
#        import pdb
#        pdb.set_trace()
        frame_data = self.controller.grab()
        data = [DataFromPlugins(name='simu_cam', data=frame_data, dim='Data2D',
                                labels=['image'], x_axis=self.x_axis,
                                y_axis=self.y_axis), ]
        self.dte_signal.emit(DataToExport('simu_cam', data=data))

    def stop(self):
        """Stop the current grab hardware wise."""
        self.emit_status(ThreadCommand('Update_Status', ['Stopped camera']))
        return ''


if __name__ == '__main__':
    main(__file__)
