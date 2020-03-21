import sys 		# OS System
from helpers import *

# Globals variables
show  = Show()
points = []

# Methods

# Create shape with coords into canvas
def create_shapes(list_of_tuples, shape):
	new_line = []
	for item in list_of_tuples:
		new_line.append( (item[0], item[1], shape) )
	return new_line

# Prepare line depend of user input
def get_line(x1,y1,x2,y2):
    # Initial conditions
    dimension_x= x2 - x1
    dimension_y = y2 - y1

    # Steep the line
    is_steep = abs(dimension_y) > abs(dimension_x)

    # Rotate line depends on -> C w h
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

	# Swapped the steps
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dimension_x = x2 - x1
    dimension_y = y2 - y1

    # Error handling
    error = int(dimension_x / 2.0)
    step_y = 1 if y1 < y2 else -1

    # Create the points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dimension_y)
        if error < 0:
            y += step_y
            error += dimension_x

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points

# Prepare canvas depends of line coords and define shape
def get_canvas(x,y):
	# Define start coords for canvas
	xa = 0
	ya = 0

	xb = x
	yb = 0

	xc = x
	yc = y

	xd = 0
	yd = y

	# Create lines depends of user input
	canvas_line1 = get_line (xa,ya,xb,yb)
	canvas_line2 = get_line (xb,yb,xc,yc)
	canvas_line3 = get_line (xc,yc,xd,yd)
	canvas_line4 = get_line (xa,ya,xd,yd)

	# Adds shape for show
	shape_canvas_line1 = create_shapes(canvas_line1,'.')
	shape_canvas_line2 = create_shapes(canvas_line2,'.')
	shape_canvas_line3 = create_shapes(canvas_line3,'.')
	shape_canvas_line4 = create_shapes(canvas_line4,'.')

	# Return one list of shape tuples
	return shape_canvas_line1 + shape_canvas_line2 + shape_canvas_line3 + shape_canvas_line4

# Show line on canvas
def draw_line(line_input):
	# L x1 y1 x2 y2
	line_input = line_input.split()

	line = get_line(int(line_input[1]),int(line_input[2]),int(line_input[3]),int(line_input[4]))
	# Print shape (x)
	shapes_line = create_shapes(line,'x')

	replace_points(shapes_line)
	# Draw on canvas
	restart(True)

# Create canvas depends on coords from user input
def draw_canvas(canvas_input):
	# C w h
	canvas_input = canvas_input.split()

	# Calculate canvas place
	global border_canvas
	global dimension_canvas
	border_canvas = int(canvas_input[1])
	dimension_canvas = int(canvas_input[2])
	canvas_place = init_canvas_place(border_canvas,dimension_canvas)
	add_points(canvas_place)

	# Calculate border
	canvas_border = get_canvas(int(canvas_input[1]),int(canvas_input[2]))
	add_points(canvas_border)
	restart(True)

# Calculates coordinates place.
def init_canvas_place(border, dimension):
	canvas_place = []
	for x in range(border-1,0,-1):
		for y in range (dimension-1,0,-1):
			canvas_place += [(x,y,' ')]
	return canvas_place

# Adds glopabl points for canvas
def add_points(list_of_tuples):
	global points

	for k,v in enumerate(list_of_tuples):
		set_point(v[0], v[1], v[2])

	points += list_of_tuples
	points = list(set(points))

	return points

#  Changes global points for canvas
def replace_points(list_of_tuples):
	global points

	for k,v in enumerate(list_of_tuples):
		set_point(v[0], v[1], v[2])
	points = list(set(points)) #
	return points

# Returns: Checks if params are in global points and returns shape
def get_point(x,y):
	for k,v in enumerate(points):
		if x == v[0] and y == v[1]:
			return v[2]
	return False

# Returns: Checks if params are in points and changes shape
def set_point(x,y, newShape):
	global points

	for k,v in enumerate(points):
		if (x,y) == (v[0],v[1]):
			del points[k]
			points += [(x,y,newShape)]
			return True
	return False

# Hard part for show neighbor element on canvas
def draw_four_neighbor(x, y, old_shape, new_shape):
	if (get_point(x,y) == oldShape):
		set_point(x, y, newShape)
		draw_four_neighbor(x, y + 1, old_shape, new_shape); # below
		draw_four_neighbor(x, y - 1, old_shape, new_shape); # above
		draw_four_neighbor(x - 1, y, old_shape, new_shape); # left
		draw_four_neighbor(x + 1, y, old_shape, new_shape); # right
	return

# Creates a console output for user to see.
def plot_points():
	points.sort()
	print(show.clear_screen)

	for k,v in enumerate(points):

		x     = v[0]
		y 	  = v[1]
		shape = v[2]

		if k > 0 and x != points[k-1][0]:
			print("")
		print(shape, end="")
	print("")

def handle_user_input_error():
	print(show.clear_screen)
	print('Wrong Input Format! Use [C w h], [L x1 x2 y1 y2], [R x1 x2 y1 y2], [B x y] or [Q]')
	restart(False)

def handle_no_canvas_error():
	print(show.clear_screen)
	print('Draw a Canvas First!')
	restart(False)

def handle_user_input(user_input):
	userInputType = user_input.split()[0]

	if userInputType == 'C':
		if len(user_input.split()) != 3:
			handle_user_input_error()
		else:
			draw_canvas(user_input)

	if userInputType == 'L':

		if len(user_input.split()) != 5:
			handle_user_input_error()
		if len(points) == 0:
			handle_no_canvas_error()
		else:
			draw_line(user_input)

	if userInputType == 'R':
		if len(user_input.split()) != 5:
			handle_user_input_error()
		if len(points) == 0:
			handle_no_canvas_error()

	if userInputType == 'B':

		if len(user_input.split()) != 4:
			handle_user_input_error()
		if len(points) == 0:
			handle_no_canvas_error()

	if userInputType == 'Q':

		if len(user_input.split()) != 1:
			handle_user_input_error()
		else:
			sys.exit(0)

def restart(plot):
	if len(points) != 0 and plot is True:
		plot_points()
	user_input = input('[Canvas] [Line] [Rectangle] [Bucketfill] [Quit]')
	handle_user_input(user_input)
