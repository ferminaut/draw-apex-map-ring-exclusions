# draw-apex-map-ring-exclusions
Determine where the ring cant go in Apex Legends. Contains a sample app that can be used to draw where the rings cant go.

This is pretty much a proof of concept. This assumes you have some OK computer science skills/know a bit of python.

# apex-ring-restrictions


Steps:

Download the TitanFall VPK Tool to extract the vpk. Available here: https://cra0.net/blog/posts/archived/2014/titanfall-vpk-tool/

Open the tool, go into your Apex Legends directory, and look for a `vpk` folder (example `C:\Apex\vpk`). This will contain a lot of files, and you can only open the files ending with _dir.

You'll see files for each map. We'll look at the `divided moon` map (aka broken moon). Open `englishclient_mp_rr_divided_moon.bsp.pak000_dir.vpk` within TitanFall VPK Tool.

This will load the files in the tool. Now right click on `maps/` and hit "Extract". Extract the files to some directory. This will extract quite a few files, and a bunch of bsp_lumps. You can further extract the bsp_lumps using bsp_tool (located here https://github.com/snake-biscuits/bsp_tool).

For ring data, we dont even have to go further than this.

After extracting the data using TitanFall VPK Tool, you'll have a folder containing the `maps/` data. Look for the `mp_rr_divided_moon_script.ent` file. This contains all the coordinates for where rings cannot go.

Example:
```
{
"editorclass" "info_survival_invalid_end_zone"
"spawnflags" "0"
"gamemode_survival" "1"
"gamemode_freedm" "1"
"gamemode_control" "1"
"gamemode_arenas" "1"
"scale" "1"
"angles" "0 90 0"
"origin" "-6544 -3920 1344"
"script_radius" "2500"
"classname" "script_ref"
}
```

From here, you can run a grep command to extract all the `info_survival_invalid_end_zone` coordinates.

`grep -B1 -A11 'info_survival_invalid_end_zone' mp_rr_divided_moon_script.ent`

Then you can just get the coordinates and the radius:

`grep -B1 -A11 'info_survival_invalid_end_zone' mp_rr_divided_moon_script.ent | grep "origin\|script_radius" > invalid_end_zones.txt`

Then write a python program to draw this on a image. I've attached my hacked together python app. It requires opencv (`pip3 install opencv-python`).

Drop a map file (`map.png`) into the directory. Adjust the map size in the python app to be the image size of the file (or for a bonus, just use a python library to read size).

Run the app and look at the map. If circles are wildly off, or they get worse at the edges, adjust the x/y factor and the x/y offset to account for different map/map geometry.



