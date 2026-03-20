from glob import glob
from setuptools import setup

package_name = 'beta_pilot_launch_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # INSTALL LAUNCH FILES
        ('share/' + package_name + '/launch', glob('launch/*.py')),
        # INSTALL RVIZ FILES
        ('share/' + package_name + '/rviz', glob('rviz/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='student20',
    maintainer_email='PRATHAPSK@HOTMAIL.COM',
    description='Launch package for robot and controller',
    license='Apache License 2.0',
    entry_points={
        'console_scripts': [],
    },
)
