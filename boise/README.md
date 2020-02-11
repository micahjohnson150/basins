# Boise River Basin

Modeling the Boise River Basin

The project contains a folder containing script to generate the topo.nc and
shapefiles for the Boise River Basin specifically used for
modeling with AWSM.

For more info on using the scripts for generating the topo see:
./topo/README.md

## Data
 * **DEM** - All DEM data is pulled from the URLS in ./topo/dem_sources.txt
 * **Vegetation Data** - All vegetation data is current defaulted to pull from landfire. More info at https://www.landfire.gov/vegetation.php
 * **Projection info** - All projections should be in EPSG 32611 for final use. For more info see https://spatialreference.org/ref/epsg/32611/

## Software
* [basin_setup  V0.13.2](https://github.com/USDA-ARS-NWRC/basin_setup/tree/v0.13.2)

## Credit
The project structure was generated using the [awsm_cookiecutter](https://github.com/USDA-ARS-NWRC/awsm_cookiecutter)
All the software used for generating the modeling file was written under
opensource licenses at the USDA-ARS-NWRC in Boise Idaho.

## Contact
* **Project started**: 2020-02-07
* **Originally Setup By**: Micah Johnson
* **Email**: micah.johnson150@gmail.com
