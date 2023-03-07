import pygame
import math
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import numpy

from include import Satellite_class
from include import GroundStation_class
from include import Observation_class
from include import satcompute

class Display:
    _sat_list = []
    _sat_commnicate_path = []
    _sat_commnicate_delay = []
    _gs: GroundStation_class.GroundStation
    _gd: Observation_class.Observation


    _scale_rate = 1000000       # store the scale of coordinate changed from ECI
    _qobj = gluNewQuadric()


    # setter of point info
    @classmethod
    def set_point_info(cls, gd, sat_list, sat_commnicate_path, sat_commnicate_delay, gs):
        cls._sat_list = sat_list
        cls._sat_commnicate_path = sat_commnicate_path
        cls._sat_commnicate_delay = sat_commnicate_delay
        cls._gs = gs
        cls._gd = gd


    # draw the total delay withＴｅｘｔ
    @classmethod
    def __draw_decription(cls):
        font = pygame.font.SysFont('arial', 18)
        textSurface = font.render("Total Delay: " + str(cls._sat_commnicate_delay[-1]) + " sec", True, (255, 255, 66, 255), (0, 66, 0, 255))
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(5, 5)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)


    @classmethod
    def __read_texture(cls, filename):
        img = Image.open(filename)
        img_data = numpy.array(list(img.getdata()), numpy.int8)
        textID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textID)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB,
                    img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        return textID

        # draw all the sat
    @classmethod
    def __draw_ground(cls):
        # draw gd
        x, y, z = satcompute.get_ground_eci_xyz(0, cls._gd)
        x = x / cls._scale_rate
        y = y / cls._scale_rate
        z = z / cls._scale_rate

        glPushMatrix()
        glTranslatef(x, y, z)       # Move to the place
        glColor3f(0.8, 0.0, 0.8)    # Put color
        gluSphere(cls._qobj, 0.1, 20, 20)  # may set to sat_class.Re
        glPopMatrix()

        # draw gs
        x, y, z = satcompute.get_ground_eci_xyz(0, cls._gs)
        x = x / cls._scale_rate
        y = y / cls._scale_rate
        z = z / cls._scale_rate

        glPushMatrix()
        glTranslatef(x, y, z)       # Move to the place
        glColor3f(1.0, 0.6, 0.2)    # Put color
        gluSphere(cls._qobj, 0.1, 20, 20)  # may set to sat_class.Re
        glPopMatrix()


    # draw all the sat
    @classmethod
    def __draw_sat(cls):
        for s in range(len(cls._sat_list)):
            x, y, z = satcompute.get_sat_eci_xyz(0, cls._sat_list[s])

            x = x / cls._scale_rate
            y = y / cls._scale_rate
            z = z / cls._scale_rate

            glPushMatrix()

            glTranslatef(x, y, z) # Move to the place
            # Put color
            if s in cls._sat_commnicate_path:
                glColor3f(0.8, 0.0, 0.0) 
            else:
                glColor3f(0.0, 0.8, 0.0)

            gluSphere(cls._qobj, 0.1, 20, 20)  # may set to sat_class.Re

            glPopMatrix()

    
    @classmethod
    def __draw_path(cls):
        # draw line from obervation to first sat
        glPushMatrix()
        glLineWidth(3)

        to_x, to_y, to_z = satcompute.get_ground_eci_xyz(0, cls._gd)
        to_x /= cls._scale_rate
        to_y /= cls._scale_rate
        to_z /= cls._scale_rate

        from_x, from_y, from_z = satcompute.get_sat_eci_xyz(0, cls._sat_list[cls._sat_commnicate_path[0]])
        from_x /= cls._scale_rate
        from_y /= cls._scale_rate
        from_z /= cls._scale_rate
        
        glBegin(GL_LINES)
        glColor3f(0.5, 0.2, 0.2) #Put color
        glVertex3f(to_x, to_y, to_z)
        glVertex3f(from_x, from_y, from_z)
        glEnd()
        glPopMatrix()

        #   draw lines between sate path
        for p in range(len(cls._sat_commnicate_path)-1):
            glPushMatrix()
            to_x, to_y, to_z = satcompute.get_sat_eci_xyz(0, cls._sat_list[cls._sat_commnicate_path[p]])
            to_x /= cls._scale_rate
            to_y /= cls._scale_rate
            to_z /= cls._scale_rate

            from_x, from_y, from_z = satcompute.get_sat_eci_xyz(0, cls._sat_list[cls._sat_commnicate_path[p+1]])
            from_x /= cls._scale_rate
            from_y /= cls._scale_rate
            from_z /= cls._scale_rate
            
            glBegin(GL_LINES)
            glColor3f(0.5, 0.2, 0.2) #Put color
            glVertex3f(to_x, to_y, to_z)
            glVertex3f(from_x, from_y, from_z)
            glEnd()
            glPopMatrix()

        # draw line from last sat to ground station
        glPushMatrix()
        to_x, to_y, to_z = satcompute.get_sat_eci_xyz(0, cls._sat_list[cls._sat_commnicate_path[-1]])
        to_x /= cls._scale_rate
        to_y /= cls._scale_rate
        to_z /= cls._scale_rate

        from_x, from_y, from_z = satcompute.get_ground_eci_xyz(0, cls._gs)
        from_x /= cls._scale_rate
        from_y /= cls._scale_rate
        from_z /= cls._scale_rate
        
        glBegin(GL_LINES)
        glColor3f(0.5, 0.2, 0.2) #Put color
        glVertex3f(to_x, to_y, to_z)
        glVertex3f(from_x, from_y, from_z)
        glEnd()
        glPopMatrix()


    @classmethod
    def display(cls):      # sat_list: list, sat_commnicate_path, sat_commnicate_delay
        pygame.init()
        display = (800, 600)
        screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        pygame.display.set_caption('Satellite Path Result')
        pygame.key.set_repeat(1, 10)    # allows press and hold of buttons
        scaled_earth_radius = Satellite_class.Re/cls._scale_rate

        glEnable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -20 - scaled_earth_radius)    # sets initial zoom so we can see globe


        glMatrixMode(GL_MODELVIEW)
        viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glLoadIdentity()

        lastPosX = 0
        lastPosY = 0
        texture = cls.__read_texture('include/earth_texture.jpg')

        while True:
            glLoadIdentity()

            # init the view matrix
            glPushMatrix()
            glLoadIdentity()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()


                # Rotation with arrow keys
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        glRotatef(10, 0, 10, 0)
                    if event.key == pygame.K_RIGHT:
                        glRotatef(10, 0, -10, 0)
                    if event.key == pygame.K_UP:
                        glRotatef(10, -10, 0, 0)
                    if event.key == pygame.K_DOWN:
                        glRotatef(10, 10, 0, 0)

                # Zoom in and out with mouse wheel
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:  # wheel rolled up
                        glScaled(1.05, 1.05, 1.05)
                    if event.button == 5:  # wheel rolled down
                        glScaled(0.95, 0.95, 0.95)

                # Rotate with mouse click and drag
                if event.type == pygame.MOUSEMOTION:
                    x, y = event.pos
                    dx = x - lastPosX
                    dy = y - lastPosY
                    mouseState = pygame.mouse.get_pressed()
                    if mouseState[0]:

                        modelView = (GLfloat * 16)()
                        mvm = glGetFloatv(GL_MODELVIEW_MATRIX, modelView)

                        # To combine x-axis and y-axis rotation
                        temp = (GLfloat * 3)()
                        temp[0] = modelView[0]*dy + modelView[1]*dx
                        temp[1] = modelView[4]*dy + modelView[5]*dx
                        temp[2] = modelView[8]*dy + modelView[9]*dx
                        norm_xy = math.sqrt(temp[0]*temp[0] + temp[1]
                                            * temp[1] + temp[2]*temp[2])
                        glRotatef(math.sqrt(dx*dx+dy*dy),
                                temp[0]/norm_xy, temp[1]/norm_xy, temp[2]/norm_xy)

                    lastPosX = x
                    lastPosY = y
                
            # multiply the current matrix by the get the new view matrix and store the final vie matrix 
            glMultMatrixf(viewMatrix)
            viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

            # apply view matrix
            glPopMatrix()
            glMultMatrixf(viewMatrix)

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT) #Clear the screen

            glPushMatrix()

            glTranslatef(0, 0, 0) #Move to the place, y may = -scaled_earth_radius
            # glColor4f(0.5, 0.2, 0.2, 1) #Put color
            # gluSphere(cls._qobj, scaled_earth_radius, 32, 16) #Draw cls._qobj

            gluQuadricTexture(cls._qobj, GL_TRUE)
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, texture)
            glColor3f(0.5, 0.2, 0.2) #Put color
            gluSphere(cls._qobj, scaled_earth_radius, 50, 50)  # may set to sat_class.Re
            glDisable(GL_TEXTURE_2D)


            glPopMatrix()

            cls.__draw_ground()

            cls.__draw_sat()

            cls.__draw_path()

            cls.__draw_decription()

            pygame.display.flip() #Update the screen
            pygame.time.wait(10)
