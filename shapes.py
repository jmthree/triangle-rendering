''' All the shapes used in the drawing program.
    When run from the command line, this executes all the tests embeded
    in the codument strings of each function.
'''
__all__ = ['triangle', 'vector', 'color']

from math import sin, cos, pi
from collections import namedtuple

class InvalidColor(Exception):
    ''' Thrown when given invalid color data '''

# Some Python magic here. Creates classes with the given names and accessors
# We use these as bases to build up on later
VectorBase   = namedtuple('VectorBase', 'x y z')
TriangleBase = namedtuple('TriangleBase', 'v0 v1 v2 c0 c1 c2')
ColorBase    = namedtuple('color', 'r g b')

class vector(VectorBase):
    ''' Represents a 3D vector. Can be 2D if the given z is 0 '''

    @property
    def length(self):
        ''' Computes the length of this vector

        >>> basis_x = vector(1, 0, 0)
        >>> basis_x.length
        1.0
        '''
        if not hasattr(self, '__length'):
            self.__length = (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
        return self.__length

    def normalize(self):
        ''' Computes the normalized version of this vector and returns it

        >>> basis_x = vector(1, 0, 0)
        >>> basis_x.normalize() == basis_x
        True
        >>> vector(3, 4, 5).normalize()
        <vector x:0.4243 y:0.5657 z:0.7071>
        '''
        length = self.length
        return vector(self.x / length, self.y / length, self.z / length)

    def cross(self, other):
        ''' Computes the cross product of this vector and the given
            vector, and returns a new vector as a result

        >>> basis_x = vector(1, 0, 0)
        >>> basis_y = vector(0, 1, 0)
        >>> basis_z = vector(0, 0, 1)
        >>> basis_x.cross(basis_y) == basis_z
        True
        >>> basis_y.cross(basis_z) == basis_x
        True
        >>> basis_z.cross(basis_y) == basis_x * -1
        True
        >>> basis_x.cross(basis_x) == vector(0, 0, 0)
        True
        '''
        new_x = self.y * other.z - self.z * other.y
        new_y = self.z * other.x - self.x * other.z
        new_z = self.x * other.y - self.y * other.x
        return vector(new_x, new_y, new_z)

    def dot(self, other):
        ''' Computes the dot product of this vector and the given
            vector, and returns number as the result

        >>> basis_x = vector(1, 0, 0)
        >>> basis_y = vector(0, 1, 0)
        >>> basis_z = vector(0, 0, 1)
        >>> basis_x.dot(basis_x)
        1
        >>> basis_x.dot(basis_y)
        0
        '''
        return self.x * other.x + self.y * other.y + self.z * other.z

    def scale(self, sc):
        ''' Scales this vector by the given number and returns a new vector
            as a result

        >>> basis_x = vector(1, 0, 0)
        >>> basis_x.scale(5) == vector(5, 0, 0)
        True
        '''
        return vector(self.x * sc, self.y * sc, self.z * sc)
    # Python magic to allow things like 5 * vector(1, 0, 0)
    __mul__ = scale

    def add(self, other):
        ''' Adds this vector to the given vector and returns a new vector
            as the result

        >>> vector(1, 2, 3).add(vector(1, 2, 3))
        <vector x:2.0000 y:4.0000 z:6.0000>
        '''
        return vector(self.x + other.x, self.y + other.y, self.z + other.z)
    # Python magic to allow v1 + v2 and v1 - v2
    __add__ = add
    __sub__ = lambda self, other: self + (other * -1)

    def rotate_x(self, degrees):
        ''' Rotates this vector by the given amount of degrees about the x-axis
            and return the resulting vector

        >>> v = vector(1, 2, 3)
        >>> v.rotate_x(90)
        <vector x:1.0000 y:-3.0000 z:2.0000>
        >>> v.rotate_x(180)
        <vector x:1.0000 y:-2.0000 z:-3.0000>
        '''
        radians = degrees / 180.0 * pi
        new_y = self.y * cos(radians) - self.z * sin(radians)
        new_z = self.y * sin(radians) + self.z * cos(radians)
        return vector(self.x, new_y, new_z)

    def rotate_y(self, degrees):
        ''' Rotates this vector by the given amount of degrees about the y-axis
            and return the resulting vector

        >>> v = vector(1, 2, 3)
        >>> v.rotate_y(90)
        <vector x:3.0000 y:2.0000 z:-1.0000>
        >>> v.rotate_y(180)
        <vector x:-1.0000 y:2.0000 z:-3.0000>
        '''
        radians = degrees / 180.0 * pi
        new_x = self.x * cos(radians) + self.z * sin(radians)
        new_z = self.z * cos(radians) - self.x * sin(radians)
        return vector(new_x, self.y, new_z)

    def __repr__(self):
        return "<vector x:%.4f y:%.4f z:%.4f>" % self


class color(ColorBase):
    ''' A simple red, green, blue color '''

    def __new__(cls, r, g, b):
        ''' Makes sure the color data is valid

        >>> x = color(1, 1, 1)
        >>> y = color(2, 1, 1)
        Traceback (most recent call last):
        ...
        InvalidColor: red value 2 not between 0 and 1
        '''
        for n, v in zip(['red', 'green', 'blue'], [r, g, b]):
            if not 0 <= v <= 1:
                raise InvalidColor("%s value %s not between 0 and 1" % (n, v))
        return ColorBase.__new__(cls, r, g, b)

    def scale(self, sc):
        return color(self.r * sc, self.g * sc, self.b * sc)
    __mul__ = scale

    def __repr__(self):
        return "<color r:%s g:%s b:%s>" % self


class triangle(TriangleBase):
    ''' Represents a 3d triangle with colors at each vertex '''

    @property
    def is_ccw(self):
        ''' Is this triangle's orientation counter clock wise?
        >>> a = vector(0, 0, 0)
        >>> b = vector(1, 0, 0)
        >>> c = vector(0, 1, 0)
        >>> blue = color(0, 0, 1)
        >>> t1 = triangle(a, b, c, blue, blue, blue)
        >>> t1.is_ccw
        True
        >>> t2 = triangle(a, c, b, blue, blue, blue)
        >>> t2.is_ccw
        False
        '''
        if not hasattr(self, '__is_ccw'):
            n = (self.v1 - self.v0).cross(self.v2 - self.v0)
            self.__is_ccw = (n.dot(vector(0, 0, 1)) > 0)
        return self.__is_ccw

    def as_pairs(self):
        ''' Returns an iterable of tuples of vector, color pairs
            from this triangle

        >>> a = vector(0, 0, 0)
        >>> b = vector(1, 0, 0)
        >>> c = vector(0, 1, 0)
        >>> blue = color(0, 0, 1)
        >>> t = triangle(a, b, c, blue, blue, blue)
        >>> for v, c in t.as_pairs():
        ...    v, c
        (<vector x:0.0000 y:0.0000 z:0.0000>, <color r:0 g:0 b:1>)
        (<vector x:1.0000 y:0.0000 z:0.0000>, <color r:0 g:0 b:1>)
        (<vector x:0.0000 y:1.0000 z:0.0000>, <color r:0 g:0 b:1>)
        '''
        return zip(self[0:3], self[3:6])

    def flat_shade(self, light_vector):
        n = (self.v1 - self.v0).cross(self.v2 - self.v0)
        n_hat = n.normalize()
        incident_vector = light_vector * -1
        shade_value = n_hat.dot(incident_vector)
        return triangle(self.v0, self.v1, self.v2, self.c0 * shade_value,
                        self.c1 * shade_value, self.c2 * shade_value)

    def rotate_x(self, degrees):
        new_v0 = self.v0.rotate_x(degrees)
        new_v1 = self.v1.rotate_x(degrees)
        new_v2 = self.v2.rotate_x(degrees)
        return triangle(new_v0, new_v1, new_v2, self.c0, self.c1, self.c2)

    def rotate_y(self, degrees):
        new_v0 = self.v0.rotate_y(degrees)
        new_v1 = self.v1.rotate_y(degrees)
        new_v2 = self.v2.rotate_y(degrees)
        return triangle(new_v0, new_v1, new_v2, self.c0, self.c1, self.c2)

    def scale(self, sc):
        return triangle(self.v0 * sc, self.v1 * sc, self.v2 * sc, self.c0, self.c1, self.c2)

    def __repr__(self):
        return "<triangle v0:%s v1:%s v2:%s c0:%s c1:%s c2:%s>" % self


if __name__ == "__main__":
    import doctest
    doctest.testmod()
