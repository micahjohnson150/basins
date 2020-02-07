############################# INPUTS ###########################################
DEM_SOURCE := dem_sources.txt
BASIN_NAME := Boise River Basin
POUR_POINTS := pour_points.bna
EPSG := 32611

# LEFT BOTTOM, RIGHT TOP
MAX_EXTENT := 571432.876 4783229.575 692327.904 4885396.130

DELINEATE_THRESHOLD := 1000000 10000000
DELINEATE_RESOLUTION := 10
NTHREADS := 2

# Vegetation Data path
VEG_DATA := /Downloads/US_140EVT_20180618/

# LEFT BOTTOM RIGHT TOP
# BASIN_EXTENT := 283967.6875 4050545 381092 4120020
################################################################################

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
							--cell_size 100 \
							-d /Downloads \
							--bypass_veg

gis_package:
	# Build a GIS package for bundle zip files
	zip $(ZIP) ./delineation/*basin_outline.* ./delineation/*_subbasin.*

qgis:
	# Make a QGIS basin project
	# Make the hillshade
	gdaldem hillshade $(DEM_IMG) ./dem/hillshade.tif
	mkdir -p ./colormaps

	# Make the DEM colormap
	cd colormaps & make_dem_colormap $(DEM_IMG)

	# Make the Vegetation colormap
	cd colormaps && make_veg_type_colormap  $(VEG_DATA)

	# Make the final project file
	make_qgis_proj -t $(DEM_IMG) \
										./dem/hillshade.tif \
										-s $(POUR_POINTS) \
										./delineation/*basin*.shp \
										./delineation/streamflow/thresh_$(MIN_THRESH)/net_thresh_*.shp \
										-n basin_setup/topo.nc \
										-v veg_type dem \
										--epsg $(EPSG)
clean_all:
	rm -rf dem basin_setup delineation
