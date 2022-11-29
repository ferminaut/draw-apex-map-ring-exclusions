# this was written in a few minutes, dont complain if it no longer works. It's only used for drawing on an image.
# this assumes some python knowledge
import cv2
import re

coordinates = []

# these are the coordinates for the game maps, these are assumptions based on the data I found
max_x = 42560
max_y = 42560
min_x = -42560
min_y = -42560

# this is the size of your map file. If you extract the map from the game files, it seems this is 4256x4256.
# make this match your map file
map_x = 4256
map_y = 4256

# These are minor offsets because the map at 0,0 top left doesnt perfectly match with the real data
# (map geometry is different)
x_offset = 115
y_offset = 32

# edge adjustment. Adjust these values slightly to adjust the accuracy at the edge of the map. I found this necessary
# to have a accurate map. it might not be necessary depending on which map file you use.
x_adj_factor = 1.015
y_adj_factor = 1.015

# This
scale_x = ((abs(min_x) + max_x + x_offset) / map_x)
scale_y = ((abs(min_y) + max_y + y_offset) / map_y)


# simple object to store the xyz+radius
class InvalidEndZone:
    x = None
    y = None
    z = None
    radius = None


# This parses the data into a list of InvalidEndZone objects
with open('invalid_end_zones.txt') as f:
    thisline = InvalidEndZone()
    for line in f.readlines():
        if "origin" in line:
            result = re.search('origin" "(.*)"', line)
            xyz = result.group(1).split()
            thisline.x = int(float(xyz[0]))

            # the following line is where the only tricky part comes in. You need to transform the y axis origin point
            thisline.y = int(float(xyz[1]) * -1)

            # z is unused
            thisline.z = int(float(xyz[2]))

        if "script_radius" in line:
            result = re.search('script_radius" "(.*)"', line)
            thisline.radius = int(result.group(1))

            # this pair is done, push into a map
            coordinates.append(thisline)
            thisline = InvalidEndZone()

# have a copy of the map handy, in my example I used a broken moon map that was 4256x4256
img = cv2.imread('map.png')

# now start drawing the circles
for restriction in coordinates:
    # draw some circles
    print(scale_x)
    print(scale_y)
    x_coord = int(((restriction.x + abs(max_x)) / scale_x) / x_adj_factor)
    y_coord = int(((restriction.y + abs(max_y)) / scale_y) / y_adj_factor)
    # draw the circle on the map
    img = cv2.circle(img, (x_coord + x_offset, y_coord + y_offset), int(restriction.radius / 19), (0, 255, 0), 5)

cv2.imshow('image', img)
cv2.waitKey()
