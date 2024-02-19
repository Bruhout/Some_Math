from supp import *
"""
This module does all the backend computation for the linear programming problem visual guide.

I would say its pure python code but you do need numpy. Some math operations I have imported from another file i wrote. and that
one uses numpy.

Note: A line is represented by 2 data structures.
----------
    1. A list of 3 elements. ax+by+c=0 is the general equation of the line.
        then the line is given as [a, b, c]
    2. A list of 2 points that the line passes through.
        point1=[x1, y1, z1]
        point2=[x2, y2, z2]
        line=[point1, points2]
        Generally these two points are the intersections of the line with the top and bottom of the screen.
        
We will keep switching between these two throughout the project.
"""



#This function will only be called by lines array. I could have made them the same function, but I didnt.
def get_line(line):
    """This function converts from the line type 1 to line type 2.
    ----------
    Args:
        line (_type_): Give in line type 1
    """
    try:
        a,b,c=line
        x1=(-c-8*b)/a
        point1=[x1, 8]
        x2=(-c+8*b)/a
        point2=[x2, -8]
        return [point1, point2]
    except ZeroDivisionError:
    ##Zero division error occurs if you try to plot parallel lines, because there is no intersection point.
        return [
            [-16,(-c/b)],
            [16,(-c/b)]
        ]



def get_lines_array(constraints):
    """This function just calls get line on all the constraints.
    It returns a list of lines, where each line is represented by 2 points.
    These 2 points are the intersection of the line with the screen top and bottom edges.

    Args:
        constraints (2 dimernsional array): A list of constraint line equations.
        Again the lines are represented as their coeffeicients in general form.

    Returns:
        _type_: _description_
    """
    lines=[]
    for constraint in constraints:
        line=get_line(constraint)
        lines.append(line)
    return lines

#This function gets the intersection points of all lines.
def get_points_array(constrains):
    points=[]
    n=len(constrains)
    for i in range(n-1):
        current_line=constrains[i]
        for k in range(i+1 ,n):
            new_line=constrains[k]
            point=two_three(get_intersection(current_line, new_line))
            points.append(point)
    return points

#This function takes in a point and computes the value of the objective function at that point.
def input_check(objective, point):
    a, b=objective
    x, y, z=point
    return (a*x+b*y)

def choose_optimal_point(points, objective, maximise=True):
    """This function takes in the objective function and corner points, and outputs the max value 
    achieved as well as the point where this value is acheived.

    Args:
        points (2D array): array containing all the corner points of the feasible region.
        objective (array): The equation of the objective function which is to be maximised/minimised.
        maximise (bool): Set to true if objective is to maximise, set to false for minimise.

    Returns:
        array: array with 2 elements
                [max/min_value, [x1, y1]]
    """
    if maximise:
        max_value=0
        max_point=0
        for i in points:
            value=input_check(objective, i)
            if value>max_value:
                max_value=value
                max_point=i
        return [max_value, max_point]
    else:
        min_value=0
        min_point=0
        for i in points:
            value=input_check(objective, i)
            if value<min_value:
                min_value=value
                min_point=i
        return [min_value, min_point]


def hex_to_rgba(hex_code: str, alpha: int):
    """This function is just used to take a hex_code for a color and convert it to a 4 array. 
    [R, G, B, alpha]

    Args:
        hex_code (str): Color hex code (RGB values). Start string with #.
        alpha (int): Integer between 0 and 255 representing tranparency.
                    225 is opaque, 0 is transparent.

    Returns:
        [R, G, B, alpha]: Pixel color array.
    --------
    
    Example:
    hex_code=#34EB7A
    alpha=100
    RGBA=hex_to_rgba(hex_code, alpha)
    
    Result:
    RGBA=[52, 235, 122, 100]
    
    """
    chars={
        '0':0,
        '1':1,
        '2':2,
        '3':3,
        '4':4,
        '5':5,
        '6':6,
        '7':7,
        '8':8,
        '9':9,
        'a':10,
        'b':11,
        'c':12,
        'd':13,
        'e':14,
        'f':15,
        'A':10,
        'B':11,
        'C':12,
        'D':13,
        'E':14,
        'F':15
    }
    
    r=chars[str(hex_code[2])]+chars[str(hex_code[1])]*16
    g=chars[str(hex_code[4])]+chars[str(hex_code[3])]*16
    b=chars[str(hex_code[6])]+chars[str(hex_code[5])]*16
    return [r, g, b, alpha]

#This function took the bulk of my effort.
#Shade takes in an inequality and shades off the region that doesnt satisfy it.
def shade(constraint, sign, hex_code="#13a6cf", alpha=100, res=[1080, 1920]):
    p, q=res
    a, b, c=constraint
    rgba=hex_to_rgba(hex_code, alpha)
    image_array=[]
    for y in range(2*p):
        row_array=[]
        for x in range(2*q):
            if sign=='>':
                condition=a*(x-q)+b*(-y+p)>(-c*135)
                if condition:
                    row_array.append(rgba)
                else:
                    row_array.append([0,0,0,0])
            else:
                condition=a*x-b*y<(-c*135)+a*q-b*p
                if condition:
                    row_array.append(rgba)
                else:
                    row_array.append([0,0,0,0])
        image_array.append(row_array)
    return np.uint8(image_array)