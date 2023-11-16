from pymodaq.control_modules.move_utility_classes import DAQ_Move_base, \
    comon_parameters_fun, main, DataActuatorType, DataActuator
from pymodaq.utils.daq_utils import ThreadCommand
from pymodaq.utils.parameter import Parameter

from pymodaq_plugins_simu_scan.hardware.simu_scan import SimuScanController


class DAQ_Move_simu_scan(DAQ_Move_base):
    """ Instrument plugin class for simulated actuators.
    
    TODO Complete the docstring of your plugin with:
        * The set of controllers and actuators that should be compatible with 
          this instrument plugin.
        * With which instrument and controller it has been tested.
        * The version of PyMoDAQ during the test.
        * The version of the operating system.
        * Installation instructions: what manufacturer’s drivers should be 
          installed to make it run?

    Attributes:
    -----------
    controller: object
        The particular object that allow the communication with the hardware, 
        in general a python wrapper around the hardware library.
         
    # TODO add your particular attributes here if any

    """
    _controller_units = 'mm'
    is_multiaxes = True
    _axes_names = SimuScanController.axes_names
    _epsilon = 1e-3
    data_actuator_type = DataActuatorType['DataActuator']

    params = [] \
        + comon_parameters_fun(is_multiaxes, axes_names=_axes_names,
                               epsilon=_epsilon)

    def ini_attributes(self):
        #  TODO declare the type of the wrapper (and assign it to
        #  self.controller) you're going to use for easy autocompletion
        self.controller: SimuScanController = None

    def get_actuator_value(self):
        """Get the current value from the hardware with scaling conversion.

        Returns
        -------
        float: The position obtained after scaling conversion.
        """
        ## TODO for your custom plugin
        axis_name = self.settings['multiaxes', 'axis']
        pos = DataActuator(data=self.controller.pos(axis_name))
        #pos = self.get_position_with_scaling(pos)
        return pos

    def close(self):
        """Terminate the communication protocol"""
        pass

    def commit_settings(self, param: Parameter):
        """Apply the consequences of a change of value in the detector settings

        Parameters
        ----------
        param: Parameter
            A given parameter (within detector_settings) whose value has been changed by the user
        """
        ## TODO for your custom plugin
        if param.name() == "a_parameter_you've_added_in_self.params":
           self.controller.your_method_to_apply_this_param_change()
        else:
            pass

    def ini_stage(self, controller=None):
        """Actuator communication initialization

        Parameters
        ----------
        controller: (object)
            custom object of a PyMoDAQ plugin (Slave case). None if only one actuator by controller (Master case)

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True
        """

        self.controller = \
            self.ini_stage_init(old_controller=controller,
                                new_controller=SimuScanController())

        info = "Simu scan initialised"
        initialized = True
        return info, initialized

    def move_abs(self, value: DataActuator):
        """ Move the actuator to the absolute target defined by value

        Parameters
        ----------
        value: (float) value of the absolute target positioning
        """

        value = self.check_bound(value)
        self.target_value = value
        axis_name = self.settings['multiaxes', 'axis']
        self.controller.move(axis_name, value.value())
        self.emit_status(ThreadCommand('Update_Status',
                                       ['%s moved to %f'
                                        % (axis_name, value.value())]))

    def move_rel(self, value: DataActuator):
        """ Move the actuator to the relative target actuator value defined by value

        Parameters
        ----------
        value: (float) value of the relative target positioning
        """
        value = self.check_bound(self.current_position + value) \
            - self.current_position
        self.target_value = value + self.current_position
        axis_name = self.settings['multiaxes', 'axis']
        self.controller.move(axis_name, value.value())
        self.emit_status(ThreadCommand('Update_Status',
                                       ['%s moved to %f'
                                        % (axis_name, value.value())]))

    def move_home(self):
        """Call the reference method of the controller"""

        axis_name = self.settings['multiaxes', 'axis']
        self.controller.move(axis_name, 0)
        self.emit_status(ThreadCommand('Update_Status',
                                       ['%s moved to zero' % axis_name]))

    def stop_motion(self):
        """Stop the actuator and emits move_done signal"""
        axis_name = self.settings['multiaxes', 'axis']
        self.emit_status(ThreadCommand('Update_Status',
                                       ['Stopped motion on %s' % axis_name]))


if __name__ == '__main__':
    main(__file__)
