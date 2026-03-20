from setuptools import setup

package_name = 'beta_pilot_controller_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='student20',
    maintainer_email='PRATHAPSK@HOTMAIL.COM',
    description='Controller node for beta_pilot robot (Task 2)',
    license='Apache License 2.0',
    entry_points={
        'console_scripts': [
            'beta_pilot_controller_node = beta_pilot_controller_pkg.beta_pilot_controller_node:main'
        ],
    },
)
