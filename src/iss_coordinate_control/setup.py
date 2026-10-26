
from setuptools import find_packages, setup

package_name = 'iss_coordinate_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name],
        ),
        (
            'share/' + package_name,
            ['package.xml'],
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yasminemuniz-diaz',
    maintainer_email='batgirlmuniz@gmail.com',
    description='ISS robotic rack coordinate motion controller',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'coordinate_controller = iss_coordinate_control.coordinate_controller:main',
        ],
    },
)
