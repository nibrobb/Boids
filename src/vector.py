#!/usr/bin/env python

""" Pre-code for INF-1400

22 January 2020 Revision 5 (Vetle Hofsøy-Woie)
Removed unnecessary tuple return from intersect_circles and
intersect_rectangle_circle.

21 January 2019 Revision 4 (Joakim Alslie):
Deleted Vector2D and replaced it with pygames own Vector2-class. Applied
changes to intersect_circles and intersect_rectangle_circle to be custom for
Vector2. Applied changes to example_code avoid type-errors.

16 January 2017 Revision 3 (Mads Johansen):
Rewritten to conform to Python 3 standard. Made class iterable, added property
as_point, replaced magnitude with __abs__ (to reflect mathematical vector
notation), added rotate method.

22 January 2012 Revision 2 (Martin Ernstsen):
Reraise exception after showing error message.

11 February 2011 Revision 1 (Martin Ernstsen):
Fixed bug in intersect_circle. Updated docstrings to Python standard.
Improved __mul__. Added some exception handling. Put example code in separate
function.

"""

from pygame import Vector2
import pygame


def intersect_rectangle_circle(rec_pos, sx, sy,
                               circle_pos, circle_radius, circle_speed):
    """ Determine if a rectangle and a circle intersects.

    Only works for a rectangle aligned with the axes.

    Parameters:
    rec_pos     - A Vector2 representing the position of the rectangles upper,
                  left corner.
    sx          - Width of rectangle.
    sy          - Height of rectangle.
    circle_pos  - A Vector2 representing the circle's position.
    circle_radius - The circle's radius.
    circle_speed - A Vector2 representing the circles speed.

    Returns:
    None if no intersection. 
    If the rectangle and the circle intersect,returns a 
    normalized Vector2 pointing in the direction the circle will
    move after the collision.
    """

    # Position of the walls relative to the ball
    top = (rec_pos.y) - circle_pos.y
    bottom = (rec_pos.y + sy) - circle_pos.y
    left = (rec_pos.x) - circle_pos.x
    right = (rec_pos.x + sx) - circle_pos.x

    r = circle_radius
    intersecting = left <= r and top <= r and right >= -r and bottom >= -r

    if intersecting:
        # Now need to figure out the vector to return.
        impulse = circle_speed.normalize()

        if abs(left) <= r and impulse.x > 0:
            impulse.x = -impulse.x
        if abs(right) <= r and impulse.x < 0:
            impulse.x = -impulse.x
        if abs(top) <= r and impulse.y > 0:
            impulse.y = -impulse.y
        if abs(bottom) <= r and impulse.y < 0:
            impulse.y = -impulse.y
        return impulse.normalize()
    return None


def intersect_circles(circle_a_position, circle_a_radius,
                      circle_b_position, circle_b_radius):
    """ Determine if two circles intersect
    Parameters:
    circle_a_position       - A Vector2D representing circle A's position
    circle_a_radius    - Circle A's radius
    circle_b_position       - A Vector2D representing circle B's position
    circle_b_radius    - Circle B's radius

    Returns:
    None if no intersection.
    If the circles intersect, returns a normalized
    Vector2 pointing from circle A to circle B.
    """
    # vector from A to B
    dp1p2 = circle_b_position - circle_a_position

    if circle_a_radius + circle_b_radius >= pygame.math.Vector2.length(dp1p2):
        return dp1p2.normalize()
    else:
        return None
