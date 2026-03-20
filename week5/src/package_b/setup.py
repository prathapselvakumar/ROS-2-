from setuptools import find_packages, setup

package_name = 'package_b'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='student20',
    maintainer_email='PRATHAPSK@HOTMAIL.COM',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'node_b = package_b.package_b.node_b:main',
            'node_a = package_a.package_a.node_a:main',
        ],
    },
)
