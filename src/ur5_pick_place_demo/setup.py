from setuptools import find_packages, setup
import os

# print(f"DEBUG: CWD={os.getcwd()}")
# print(f"DEBUG: listed resource={os.listdir('resource')}")
# raise RuntimeError(f"DEBUG: CWD={os.getcwd()}, listed resource={os.listdir('resource')}")

package_name = 'ur5_pick_place_demo'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/bringup.launch.py']),
        ('share/' + package_name + '/urdf', ['ur5_pick_place_demo/ur5_simple.urdf']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='TODO: Package description',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'pick_place_demo = ur5_pick_place_demo.pick_place_demo:main',
            'republish_joint_states = ur5_pick_place_demo.joint_republisher:main',
            'scene_object_publisher = ur5_pick_place_demo.scene_object_publisher:main',
        ],
    },
)
