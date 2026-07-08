#!/usr/bin/env python
"""
| File: 3_ros2_single_vehicle.py
| Author: Marcelo Jacinto (marcelo.jacinto@tecnico.ulisboa.pt)
| License: BSD-3-Clause. Copyright (c) 2024, Marcelo Jacinto. All rights reserved.
| Description: This files serves as an example on how to build an app that makes use of the Pegasus API to run a 
simulation with a single vehicle, controlled using the ROS2 backend system. NOTE: this ROS2 interface only works on Ubuntu 22.04LTS and ROS2 Humble
"""

# Imports to start Isaac Sim from this script
import carb
from isaacsim import SimulationApp

# Start Isaac Sim's simulation environment
# Note: this simulation app must be instantiated right after the SimulationApp import, otherwise the simulator will crash
# as this is the object that will load all the extensions and load the actual simulator.
simulation_app = SimulationApp({"headless": False})

# -----------------------------------
# The actual script should start here
# -----------------------------------
import omni.timeline
from omni.isaac.core.world import World
from isaacsim.core.api import SimulationContext
import numpy as np

# from omni.isaac.core.utils.stage import add_reference_to_stage
import isaacsim.core.utils.stage as stage_utils
# from pxr import UsdGeom, Gf
# import omni.usd
from isaacsim.core.experimental.prims import RigidPrim

# Import the Pegasus API for simulating drones
from pegasus.simulator.params import ROBOTS, SIMULATION_ENVIRONMENTS

from pegasus.simulator.logic.people.person import Person
from pegasus.simulator.logic.people.person_controller import PersonController

from pegasus.simulator.logic.backends.ros2_backend import ROS2Backend
from pegasus.simulator.logic.backends.px4_mavlink_backend import PX4MavlinkBackend, PX4MavlinkBackendConfig
from pegasus.simulator.logic.graphical_sensors.monocular_camera import MonocularCamera
from pegasus.simulator.logic.graphical_sensors.lidar import Lidar
from pegasus.simulator.logic.vehicles.multirotor import Multirotor, MultirotorConfig
from pegasus.simulator.logic.interface.pegasus_interface import PegasusInterface

from scipy.spatial.transform import Rotation

class CirclePersonController(PersonController):

    def __init__(self):
        super().__init__()

        self._radius = 5.0
        self.gamma = 0.0
        self.gamma_dot = 0.3
        
    def update(self, dt: float):

        # Update the reference position for the person to track
        self.gamma += self.gamma_dot * dt
        
        # Set the target position for the person to track
        self._person.update_target_position([self._radius * np.cos(self.gamma), self._radius * np.sin(self.gamma), 0.0])
        
class PegasusApp:
    """
    A Template class that serves as an example on how to build a simple Isaac Sim standalone App.
    """

    def __init__(self):
        """
        Method that initializes the PegasusApp and is used to setup the simulation environment.
        """

        # Acquire the timeline that will be used to start/stop the simulation
        self.timeline = omni.timeline.get_timeline_interface()

        # Start the Pegasus Interface
        self.pg = PegasusInterface()
        # Set the default PX4 installation path used by the simulator
        # This will be saved for future runs
        self.pg.set_px4_path("/home/mummtaz/PX4-Autopilot")

        # Acquire the World, .i.e, the singleton that controls that is a one stop shop for setting up physics, 
        # spawning asset primitives, etc.
        self.pg._world = World(**self.pg._world_settings)
        self.world = self.pg.world

        # Launch one of the worlds provided by NVIDIA
        self.pg.load_environment(SIMULATION_ENVIRONMENTS["Warehouse"])
        # self.pg.load_environment(SIMULATION_ENVIRONMENTS["Curved Gridroom"])

        # Create the vehicle
        # Try to spawn the selected robot in the world to the specified namespace
        config_multirotor = MultirotorConfig()

        # Create the multirotor configuration
        mavlink_config = PX4MavlinkBackendConfig({
            "vehicle_id": 0,
            "px4_autolaunch": True,
            "px4_dir": self.pg.px4_path,
            "px4_vehicle_model": self.pg.px4_default_airframe # CHANGE this line to 'iris' if using PX4 version bellow v1.14
            # "px4_vehicle_model": 'iris'
        })

        config_multirotor.backends = [
            PX4MavlinkBackend(mavlink_config),
            ROS2Backend(vehicle_id=0, 
                        config={
                            "namespace": 'drone',
                            "pub_sensors": False,
                            "pub_graphical_sensors": True,
                            "pub_state": False,
                            "pub_tf": False,
                            "sub_control": False})
            ]
        
        config_multirotor.graphical_sensors = [
            MonocularCamera("camera", config={"update_rate": 10.0}),
            Lidar("lidar")
        ]
        
        Multirotor(
            "/World/quadrotor",
            ROBOTS['Iris'],
            0,
            [0.0, 0.0, 0.07],
            Rotation.from_euler("XYZ", [0.0, 0.0, 90.0], degrees=True).as_quat(),
            config=config_multirotor,
        )

        # Set the camera of the viewport to a nice position
        self.pg.set_viewport_camera([5.0, 9.0, 6.5], [0.0, 0.0, 0.0])

        # Reset the simulation environment so that all articulations (aka robots) are initialized
        self.world.reset()

        # Auxiliar variable for the timeline callback example
        self.stop_sim = False

        # self.simulation_context = SimulationContext(physics_dt=1.0 / 60.0, rendering_dt=1.0 / 60.0, stage_units_in_meters=1.0)

    def run(self):
        """
        Method that implements the application main loop, where the physics steps are executed.
        """

        # Start the simulation
        self.timeline.play()
        # self.simulation_context.play()
        

        # The "infinite" loop
        while simulation_app.is_running() and not self.stop_sim:

            # Update the UI of the app and perform the physics step
            self.world.step(render=True)
            # simulation_app.update()
        
        # Cleanup and stop
        carb.log_warn("PegasusApp Simulation App is closing.")
        self.timeline.stop()
        simulation_app.close()

def main():

    # Instantiate the template app
    pg_app = PegasusApp()

    # Run the application loop
    pg_app.run()

if __name__ == "__main__":
    main()