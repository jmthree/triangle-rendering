CS4300 Homework Four
Author: John Mendelewski <jmendel@ccs.neu.edu>
Last Revision: March 24, 2010

== INSTALLATION ==
This assignment uses python 2.6 and the pyglet rendering library.
OpenGL is used through this library. Therefore, this assignment
requires OpenGL be configured to run on the computer.

== RUNNING ==
To render only flat, colored triangles:

    python triangle2d.py <tri-file>

To render wireframe shapes:

    python wireframe.py <tri-file>

To render flat shaded shapes:

    python flatshaded.py <tri-file>

== CONTROLS ==
While in wireframe or flat shaded, use the left and right arrow
keys to rotate the shape about the y-axis, and the up and down
arrow keys to rotate it about the x-axis. Use the plus and minus
keys to scale the shape up and down.

== KNOWN BUGS ==
The program gets really slow on some of the higher resolution
files. I wanted to do the math/work myself, so my object representations
and the consistant iteration over each triangle on the screen
contributes to the slow speed. If given more time, or in an
other context, I would just fall back on pure OpenGL with its
optimized C code base.
