# Kaweah River Basin

## Project Goal
Modeling the Kaweah River Basin

# Delineating Kaweah River Basin for AWSM

This project creates the following automatically:
  * Download images and generate a single DEM image
  * Delineate the basin using pour points
  * Generate a topographic netcdf as an input to AWMS/SMRF
  * Produce QGIS projects, package GIS data and make convenient colormaps

**WARNING:** Before using this project you should know:

  * The project can only handle UTM projections
  * The project makes a lot of assumptions reagrding being within a docker
  * The script used are streamlined for basins in the U.S.

## Requirements
To setup a new basin for AWSM tends to be an iterative process. To follow this
guide you will need:
  * Docker/ Docker-compose installed
  * An internet connection
  * Pour points
  * URLS for downloading dem data

## Getting Started
Use the Makefile to modify you project and the delineation process

The first step is to copy the folder new_basin and open it Then:
1. Edit the file pour_points.bna
2. Edit the file dem_sources.txt
3. Edit the Makefile

### Add Pour Points (pour_points.bna)
Adding pour points will dictate big your basin is. There is not a limit to the
number of pour points used but there is a limitation on how many will be
represented based on the delineation threshold used. The name given to a pour
point is used to name the subbasin so name the pour point sensically.

### Getting DEM Data for the US (dem_source.txt)
* Go to https://viewer.nationalmap.gov/basic/
* Select Elevation Products
* Select 1/3 arc second-dem and under format select img data
* Zoom in on the map to approximately the area of interest.
* Select Find Products
* Under the Available products use the foot print link on each tile to see which tiles are necessary
* When you find a tile, add it to your shopping cart.
* When you are finished, Select Save as text.
* Move the file to this folder and rename to dem_sources.txt

#### Edit the Makefile Inputs
The top of the Makefile has several inputs variables which can be edited without
much concern for raising errors. They are described in the table below:

| Input Variable Name          |  Description                               |
|------------------------------|--------------------------------------------|
| **DEM_SOURCE**               |  Text file containing URLS to dem tiles to download
| **BASIN_NAME**               | Name to use for naming files, and the proper name in the final topo
| **POUR_POINTS**              | BNA file containing names of pour points which is used to name subbasins, Coordinates must be in EPSG Coordinates
| **EPSG**                     | EPSG code representing the projection information. Currently AWSM only supports UTM
| **MAX_EXTENT**               | Maximum extent to delineate on for the dem. Must be in same Coordinates as EPSG
| **DELINEATE_THRESHOLD**      | Number of cells draining into an area to constitute a subbasin (Bigger # == Bigger Subbasins). Its recommended once you find a threashold that works, divide it by ten adn add it to the beginning of the list here to add nice looking streams to the QGIS project
| **DELINEATE_RESOLUTION**     | Cellsize resolution used for delineation (Meters)
| **NTHREADS**                 | Number of processes to launch for delineating the basin

There are several make commands which can be used:

| Make commands    | Description                                               |
|------------------|-----------------------------------------------------------|
| **download_dem** | Downloads the data in the dem_sources.txt
| **dem_process**  | Make the full reprojected DEM mosaic in the project dictated by EPSG
| **delineate**    | Delineate the basin using the full dem, pour points, and delineation threshold
| **topo**         | Makes the static input netcdf for AWSM known as the topo.nc
| **gis_package**  | Creates a zip file of all the shapefiles created in the delineation
| **qgis**         | Create a hillshade, make a colormap for it and build a qgis project with it all.
| **clean_all**    | Delete all the generated data, CAUTION: This deletes the downloads too.
| **init**         | Use this command when running on an empty project, this will download and process the dems, delineate without the retry flag.
| **all**          | Rerun the delineate, topo, qgis, and gis package commands.

#### Running the Makefile
The new_basin project has been specifically configured to run in docker.
There is a pre-configured docker-compose file which describes how to mount
directories and run commands for docker. This does not need editing.
To execute the commands described above simple navigate to the project folder,
and enter into the terminal:

For linux/ OSX:
> sh ./scripts/run.sh init

For windows:
> ./scripts/run.ps1 init

**Warning**: The first time you run this script it will quite a bit of time as
you need to download you DEM tiles and the entire landfire dataset. The landfire
datasets alone take 40 mins.

If you are rerunning, use:

For linux/ OSX:
> sh ./scripts/run.sh all

For windows:
> ./scripts/run.ps1 all

If you want to focus on a specific task like delineating or something else you
can always use any of the single make functions described in the table above
with:

For linux/ OSX:
> sh ./scripts/run.sh <command>

For windows:
> ./scripts/run.ps1 <command>
