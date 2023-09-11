from setuptools import setup, find_packages


install_requires = ['pyserial']

package_name = 'a4s_sealer_driver'

setup(
    name='a4s_sealer_driver',
    version='0.0.1',
    packages=find_packages(),
    data_files=[],
    install_requires=install_requires,
    zip_safe=True,
    python_requires=">=3.8",
    maintainer='Rafael Vescovi and Doga Ozgulbas',
    maintainer_email='dozgulbas@anl.gov',
    description='Driver for the Azenta Sealer',
    url='https://github.com/AD-SDL/a4s_sealer_driver.git', 
    license='MIT License',
    entry_points={},
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
