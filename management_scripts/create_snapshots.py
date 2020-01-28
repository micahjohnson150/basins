"""
Script creates a snapshot of all the setup.qgs projects which will be useful
for figure making

Should be executed from the top level of the repo

Usage:

    python management_scripts/create_snapshots.py

Result:
    Creates a PNG in every topo folder of the GIS project which is suitable for
    figures when first generated
"""

from subprocess import check_output
from os import listdir
from os.path import isfile, join

complete = 0

# File the current dir for basins and look for everything not our management folder
basins = [b for b in listdir('./') if isfile(join(b,'topo','setup.qgs'))]

print("Generating {} basin figures...".format(len(basins)))

for basin in basins:
    setup_f = "./{0}/topo/setup.qgs".format(basin)

    # Confirm we have the setup file
    if isfile(setup_f):
        print("Creating Snapshot of {}...".format(basin))
        cmd = "qgis --snapshot {0}/topo/{0}_figure.png --project {0}/topo/setup.qgs".format(basin)
        try:
            s = check_output(cmd, shell=True)
        except:
            pass
        complete += 1
    else:
        print("Skipping {}, {} file not found...".format(basin, setup_f))
print("Completed snapshots of {}/{} requested".format(complete, len(basins)))
