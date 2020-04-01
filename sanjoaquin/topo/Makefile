############################# INPUTS ###########################################
DEM_SOURCE := dem_sources.txt
BASIN_NAME := san joaquin river basin
POUR_POINTS := pour_points.bna
EPSG := 32611

# LEFT BOTTOM, RIGHT TOP
MAX_EXTENT := 256525 4096525 353425 4179675
DELINEATE_THRESHOLD := 1000000 9500000
DELINEATE_RESOLUTION := 10
NTHREADS := 2

# LEFT BOTTOM RIGHT TOP
BASIN_EXTENT := 256625 4096625 353325 4179575
################################################################################

# Path in the docker to the veg data
VEG_DATA := /Downloads/US_140EVT_20180618/

# Build the dem file name
DEM_IMG := ./dem/$$(python3.6 -c "print('{}_dem_EPSG{}.tif'.format('$(BASIN_NAME)'.lower(),'$(EPSG)').replace(' ','_'))")

# Build a zip file name
ZIP:=$$(python3.6 -c "print('{}_shapefile_EPSG{}.zip'.format('$(BASIN_NAME)'.lower(),'$(EPSG)').replace(' ','_'))")

# Rebuild the BASIN_NAME to look pretty
BASIN_NAME:=$$(python3.6 -c "print('{}'.format('$(BASIN_NAME)'.title()).replace('_',' '))")
MIN_THRESH:=$$(python3.6 -c "print('{}'.format('$(DELINEATE_THRESHOLD)'.split(' ')[0]))")

all:
	make delineate
	make topo
	make qgis
	make gis_package

init:
	# Download and build dem
	make download_dem
	make dem_process
	# Delineate without the rerun
	delineate -p $(POUR_POINTS) \
						-d $(DEM_IMG) \
						-t $(DELINEATE_THRESHOLD) \
						-n $(NTHREADS) \
						-strm
	make topo
	make qgis
	make gis_package

# Download the dems in the source file
download_dem:
	# Make a directory and download data to it from the National Elevation Dataset
	mkdir -p dem
	echo Downloading
	while read img ; do \
		echo $$img ; \
		wget -P dem -nc $$img ; \
	done <$(DEM_SOURCE)

MOSAIC:=./dem/mosaic.img
FULL_DEM:=./dem/full_dem_$(EPSG).tif

dem_process:
	# Unzip all the dems
	unzip -u -o './dem/*.zip' -d ./dem
	# Merge all images to a single image
	gdal_merge.py -o $(MOSAIC) dem/*.img
	# Reproject the image and overwrite
	gdalwarp -overwrite \
					 -t_srs EPSG:$(EPSG) \
					 -tr $(DELINEATE_RESOLUTION) $(DELINEATE_RESOLUTION) \
					 -te $(MAX_EXTENT) \
					 -r bilinear \
					 $(MOSAIC) \
					 $(DEM_IMG)

	# Clean up some processing images
	rm $(MOSAIC)

delineate:
	# Delineate the basin
	delineate -p  $(POUR_POINTS) \
						-d $(DEM_IMG) \
						-t $(DELINEATE_THRESHOLD) \
						-n $(NTHREADS) \
						-strm \
						--rerun

topo:

	# Generate the topo file for SMRF/AWSM
	basin_setup -f  delineation/basin_outline.shp \
							-bn $(BASIN_NAME) \
							-sb delineation/*_subbasin.shp \
							-dm $(DEM_IMG) \
							--extent $(BASIN_EXTENT) \
							-d /Downloads

gis_package:
	# Build a GIS package for bundle zip files
	zip $(ZIP) ./delineation/*basin_outline.* ./delineation/*_subbasin.*


VEG_LAYER:=veg_type.tif

veg_process:
	# Crop veg data for GIS
	gdalwarp  -t_srs EPSG:$(EPSG) \
	 				  -overwrite \
						-te $(MAX_EXTENT) \
						-tr $(DELINEATE_RESOLUTION) $(DELINEATE_RESOLUTION) \
						$(VEG_MOSAIC) \
						$(VEG_LAYER)

qgis:
	# Make a QGIS basin project
	# Make the hillshade
	gdaldem hillshade $(DEM_IMG) ./dem/hillshade.tif
	mkdir -p ./colormaps

	# Make the DEM colormap
	make_dem_colormap $(DEM_IMG)

	# Make the Vegetation colormap
	make_veg_type_colormap $(VEG_DATA)

	# Move them to the colormaps directory
	mv *.qml colormaps/.

	# Make the veg data
	make veg_process

	# Make the final project file
	make_qgis_proj -t $(VEG_LAYER) \
										$(DEM_IMG) \
										./dem/hillshade.tif \
										-s $(POUR_POINTS) \
										./delineation/*basin*.shp \
										./delineation/streamflow/thresh_$(MIN_THRESH)/net_thresh_*.shp \
										-n basin_setup/topo.nc \
										-v veg_type dem \
										--epsg $(EPSG)

geoserver:
	cd delineation && \
	guds -f *_subbasin.shp -b sanjoaquin -c ~/geoserver.json -t shapefile

clean_all:
	rm -rf dem basin_setup delineation
