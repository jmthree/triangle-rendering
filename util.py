''' Utility functions used throughout the graphics program '''

import sys
from os import path

from shapes import triangle, vector, color, InvalidColor

def parse_triangle_data(tri_lines):
    ''' Takes in a iterable of lines, each line triangle data.
        Creates triangles, with vectors and colors, for each valid line
        Returns the created triangles, and an array of error data if any
    '''
    triangles = []
    invalid_lines = []
    for num, line in enumerate(tri_lines):
        data = line.strip()
        if data and data[0] != "#":
            values = [float(x) for x in data.split(" ")]
            if len(values) == 18:
                point0 = vector(*values[0:3])
                point1 = vector(*values[3:6])
                point2 = vector(*values[6:9])
                try:
                    col0   = color(*values[9:12])
                    col1   = color(*values[12:15])
                    col2   = color(*values[15:18])
                except InvalidColor, ex:
                    invalid_lines.append((num + 1, data, str(ex)))
                else:
                    # If there were no color problemss, make the triangle
                    tri = triangle(point0, point1, point2, col0, col1, col2)
                    triangles.append(tri)
    return triangles, invalid_lines


def load_triangle_file(program_name, args):
    ''' Loads a triangle file in from the command line and returns all
        the parsed triangle objects contained in that file. If the file
        contains any errors, they are printed out to the command line.
    '''
    def display_usage(error):
        " Displays a usage message with the passed error message, then exits "
        print error
        print "usage: %s <tri-file>" % program_name
        sys.exit(-1)

    if len(args) != 1:
        display_usage("Invalid number of arguments")
    trifile = args[0]
    if not path.exists(trifile):
        display_usage("File %s does not exist" % trifile)
    with open(trifile) as trilines:
        triangles, errors = parse_triangle_data(trilines)
        if errors:
            print "=== Errors ==="
            for error in errors:
                print "Invalid line num %s: %s.\n\tError: %s" % error
    return triangles
