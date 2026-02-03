

`docker exec -it ur5_sim /bin/bash`

`cd src`

`colcon build --symlink-install`

`source install/setup.bash`


## Launch the combined bringup (robot_state_publisher, republisher, demo):

`ros2 launch ur5_pick_place_demo bringup.launch.py`