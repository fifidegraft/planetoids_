"""
Models module for Planetoids

This module contains the model classes for the Planetoids game. Anything that you
interact with on the screen is model: the ship, the bullets, and the planetoids.

We need models for these objects because they contain information beyond the simple
shapes like GImage and GEllipse. In particular, ALL of these classes need a velocity
representing their movement direction and speed (and hence they all need an additional
attribute representing this fact). But for the most part, that is all they need. You
will only need more complex models if you are adding advanced features like scoring.

You are free to add even more models to this module. You may wish to do this when you
add new features to your game, such as power-ups. If you are unsure about whether to
make a new class or not, please ask on Ed Discussions.

# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""
from consts import *
from game2d import *
from introcs import *
import math

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py. If you need extra information from Gameplay, then it should be a 
# parameter in your method, and Wave should pass it as a argument when it calls 
# the method.

# START REMOVE
# HELPER FUNCTION FOR MATH CONVERSION
def degToRad(deg):
    """
    Returns the radian value for the given number of degrees
    
    Parameter deg: The degrees to convert
    Precondition: deg is a float
    """
    return math.pi*deg/180
# END REMOVE


class Bullet(GEllipse):
    """
    A class representing a bullet from the ship
    
    Bullets are typically just white circles (ellipses). The size of the bullet is 
    determined by constants in consts.py. However, we MUST subclass GEllipse, because 
    we need to add an extra attribute for the velocity of the bullet.
    
    The class Wave will need to look at this velocity, so you will need getters for
    the velocity components. However, it is possible to write this assignment with no 
    setters for the velocities. That is because the velocity is fixed and cannot change 
    once the bolt is fired.
    
    In addition to the getters, you need to write the __init__ method to set the starting
    velocity. This __init__ method will need to call the __init__ from GEllipse as a
    helper. This init will need a parameter to set the direction of the velocity.
    
    You also want to create a method to update the bolt. You update the bolt by adding
    the velocity to the position. While it is okay to add a method to detect collisions
    in this class, you may find it easier to process collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    #Attribute _deleted: whether or not a bullet should be deleted
    #Invariant: _deleted is a boolean

    #Attribute _velocity: the velocity of the bullet
    #Invariant: _velocity is a Vector2 object
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    def getVelocity(self):
        """Returns the bullets's velocity attribute"""
        return self._velocity

    def getDeleted(self):
        """Returns the bullet's deleted attribute."""
        return self._deleted

    def setDeleted(self,state):
        """
        Sets the attribute deleted to valid state. State can be either
        True, if the bullet should be deleted from a list, and False otherwise.
        Parameter state: the state to set attribute deleted to
        Precondition: state is a boolean- either True or False
        """
        self._deleted=state

    def getPosition(self):
        """Returns a list of the bullet's position as 
        a list of [x-coordinate, y-coordinate].
        """
        return [self.x,self.y]

    # INITIALIZER TO SET THE POSITION AND VELOCITY
    def __init__(self,facing,x,y,width,height,fillcolor=BULLET_COLOR):               
        """
        Creates a new bullet. 

        Has facing, x, y coordinates, width, height and fillcolor.

        Precondition: facing is a Vector2 object, x and y are floats, width and 
        height, fillcolor are appropriate constants from consts.py.
        """
        super().__init__(x=x,y=y,fillcolor=BULLET_COLOR,width=width,height=height)
        facing.normalize()
        self._velocity=facing*BULLET_SPEED
        self._deleted=False
    
    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)


class Ship(GImage):
    """
    A class to represent the game ship.
    
    This ship is represented by an image. The size of the ship is determined by constants 
    in consts.py. However, we MUST subclass GEllipse, because we need to add an extra 
    attribute for the velocity of the ship, as well as the facing vecotr (not the same)
    thing.
    
    The class Wave will need to access these two values, so you will need getters for 
    them. But per the instructions,these values are changed indirectly by applying thrust 
    or turning the ship. That means you won't want setters for these attributes, but you 
    will want methods to apply thrust or turn the ship.
    
    This class needs an __init__ method to set the position and initial facing angle.
    This information is provided by the wave JSON file. Ships should start with a shield
    enabled.
    
    Finally, you want a method to update the ship. When you update the ship, you apply
    the velocity to the position. While it is okay to add a method to detect collisions 
    in this class, you may find it easier to process collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    #Attribute _velocity: the velocity of the ship
    #Invariant: _velocity is a Vector2 object

    #Attribute _facing: the facing of the ship
    #Invariant: _facing is a Vector2 object
     
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    def getVelocity(self):
        """Returns the ship's velocity attribute"""
        return self._velocity

    def getFacing(self):
        """Returns the ship's facing attribute"""
        return self._facing

    def getPosition(self):
        """Returns the ship's position as a list of 
        [x-coordinate, y-coordinate].
        """
        return [self.x,self.y]

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self,x,y,angle,width=2*SHIP_RADIUS,height=2*SHIP_RADIUS,
        source=SHIP_IMAGE):
        """
        Creates a ship object.

        Has x, y coordinates, angle, width, height and source.

        Precondition: x, y are floats, angle is loaded from the json file under 
        key ['ship']['angle'], width, height and source are constants appropriate
        from consts.py.
        """
        super().__init__(x=x,y=y,angle=angle,width=2*SHIP_RADIUS,
            height=2*SHIP_RADIUS,source=SHIP_IMAGE)
        self._velocity=Vector2(x=0, y=0)
        self._facing=Vector2(math.cos(degToRad(angle)),math.sin(degToRad(angle)))      
     
    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    def turn(self,da):
        """
        Turns the ship by da degrees.
        Parameter da: the number of degrees to turn by.
        Precondition: da is an integer.
        """
        self.angle+=da
        self._facing=Vector2(math.cos(degToRad(self.angle)),
            math.sin(degToRad(self.angle)))        

    def impulse(self):
        """
        This method sets the ship's velocity according to the impulse.
        If the resulting velocity is greater than SHIP_MAX_SPEED, then it is set
        to SHIP_MAX_SPEED.
        """
        impls=self._facing*SHIP_IMPULSE
        v=self._velocity+impls
     
        if v.length()>=SHIP_MAX_SPEED:
            self._velocity=v.normalize()
            self._velocity*=SHIP_MAX_SPEED

        else:
            self._velocity+=impls

    def turnship(self,input):
        """
        This method turns the ship depending on input. It also increases the 
        velocity accordingly.
        """
        da=0
        if input.is_key_down('left'):
            da+= SHIP_TURN_RATE
        if input.is_key_down('right'):
            da -= SHIP_TURN_RATE
        self.turn(da)
        if input.is_key_down('up'):
            self.impulse()

    def wrapship(self):
        """
        This method is used to ''wrap'' the ship when it exits the window.
        """
        if self.x<-DEAD_ZONE:
            self.x+=GAME_WIDTH+2*DEAD_ZONE
        if self.x>GAME_WIDTH+DEAD_ZONE:
            self.x-=GAME_WIDTH+2*DEAD_ZONE
        if self.y<-DEAD_ZONE:
            self.y+=GAME_HEIGHT+2*DEAD_ZONE
        if self.y>GAME_HEIGHT+DEAD_ZONE:
            self.y-=GAME_HEIGHT+2*DEAD_ZONE

                
class Asteroid(GImage):
    """
    A class to represent a single asteroid.
    
    Asteroids are typically are represented by images. Asteroids come in three 
    different sizes (SMALL_ASTEROID, MEDIUM_ASTEROID, and LARGE_ASTEROID) that 
    determine the choice of image and asteroid radius. We MUST subclass GImage, because 
    we need extra attributes for both the size and the velocity of the asteroid.
    
    The class Wave will need to look at the size and velocity, so you will need getters 
    for them.  However, it is possible to write this assignment with no setters for 
    either of these. That is because they are fixed and cannot change when the planetoid 
    is created. 
    
    In addition to the getters, you need to write the __init__ method to set the size
    and starting velocity. Note that the SPEED of an asteroid is defined in const.py,
    so the only thing that differs is the velocity direction.
    
    You also want to create a method to update the asteroid. You update the asteroid 
    by adding the velocity to the position. While it is okay to add a method to detect 
    collisions in this class, you may find it easier to process collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    
    #Attribute _deleted: whether or not an asteroid should be deleted
    #Invariant: _deleted is a boolean

    #Attribute _velocity: the velocity of the asteroid
    #Invariant: _velocity is a Vector2 object

    #Attribute _direction: the direction of the asteroid
    #Invariant: _direction is a Vector2 object
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    def getVelocity(self):
        """Returns the asteroid's velocity attribute"""
        return self._velocity

    def getDeleted(self):
        """Returns the asteroid's deleted attribute"""
        return self._deleted

    def setDeleted(self,state):
        """Sets the attribute deleted to valid state. State can be either
        True, if the bullet should be deleted from a list, and False otherwise.

        Parameter state: the state to set attribute deleted to
        Precondition: state is a boolean- either True or False
        """
        self._deleted=state

    def setVelocity(self,velocity):
        """ 
        Sets the velocity of an asteroid a given velocity.

        Parameter velocity: the velocity to set to.
        Precondition: velocity is a list of velocity x and y coordinates.
        """
        v=Vector2(velocity[0],velocity[1])
        self._velocity=v
    
    # INITIALIZER TO CREATE A NEW ASTEROID
    def __init__(self,x,y,width,height,source,direction):
        """
        Creates a new asteroid.
        
        Has x, y coordinate, width, height, source, direction.

        Precondition: x, y are floats, width, height, source are taken from 
        consts.py and direction is loaded from a json under key 
        ['asteroids']['direction'].
        """
        super().__init__(x=x,y=y,width=width,height=height,source=source) 
        self._deleted=False
        self._direction=direction 
        if direction.length()==0:
            self._velocity=Vector2(0,0)
        else:
            if source==SMALL_IMAGE:
                direction.normalize()
                self._velocity=direction*SMALL_SPEED
            if source==MEDIUM_IMAGE:
                direction.normalize()
                self._velocity=direction*MEDIUM_SPEED
            if source==LARGE_IMAGE:
                direction.normalize()
                self._velocity=direction*LARGE_SPEED

    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    def wrapasteroid(self):
        """ 
        This method ''wraps'' the asteroid when it exits the window.
        """
        if self.x<-DEAD_ZONE:
            self.x+=GAME_WIDTH+2*DEAD_ZONE
        if self.x>GAME_WIDTH+DEAD_ZONE:
            self.x-=GAME_WIDTH+2*DEAD_ZONE
        if self.y<-DEAD_ZONE:
            self.y+=GAME_HEIGHT+2*DEAD_ZONE
        if self.y>GAME_HEIGHT+DEAD_ZONE:
            self.y-=GAME_HEIGHT+2*DEAD_ZONE

    def collideshp(self,position):
        """
        This method returns True if the ship and asteroid collide,
        False otherwise.
        Parameter position: the position of the ship at the moment of collision.
        Precondition: position is a list of x and y coordinates of the ship.
        """
        x=position[0]
        y=position[1]
        distship=math.sqrt((self.x-x)**2+(self.y-y)**2)
        if distship<SHIP_RADIUS+self.width/2:               
            return True
        else:
            return False
    
    def collideblt(self,position):
        """
        This method returns True if the asteroid and a bullet collide, False
        otherwise.
        Parameter position: the position of the bullet at the moment of 
        collision.
        Precondition: position is a list of x and y coordinates of the bullet.
        """
        x=position[0]
        y=position[1]
        distbullet=math.sqrt((self.x-x)**2+(self.y-y)**2)
        if distbullet<BULLET_RADIUS+self.width/2:     
            return True
        else:
            return False

    def breakupblt(self,velocity):
        """
        This method returns a list of new asteroids that are generated after a 
        collision with a bullet.
        Parameter velocity: the bullet's velocity at the moment of collision.
        Precondition: velocity is a valid bullet velocity.
        """
        radii=[SMALL_RADIUS,MEDIUM_RADIUS,LARGE_RADIUS]
        images=[SMALL_IMAGE,MEDIUM_IMAGE,LARGE_IMAGE]
        speeds=[SMALL_SPEED,MEDIUM_SPEED,LARGE_SPEED]
        cv=velocity.normalize()
        if self.width/2!=radii[0]:
            rad=radii[radii.index(self.width/2)-1]
            img=images[radii.index(self.width/2)-1]
            speed=speeds[radii.index(self.width/2)-1]
            new1=Vector2(self.x,self.y)+cv*rad
            cv2=cv.rotation(math.pi*2/3)
            new2=Vector2(self.x,self.y)+cv2*rad
            cv3=cv.rotation(-math.pi*2/3)
            new3=Vector2(self.x,self.y)+cv3*rad
            asteroids=[Asteroid(new1.x,new1.y,rad*2,rad*2,img,cv),
                Asteroid(new2.x,new2.y,rad*2,rad*2,img,cv2),
                Asteroid(new3.x,new3.y,rad*2,rad*2,img,cv3)]
            for i in range(len(asteroids)):
                asteroids[i]._velocity=speed*asteroids[i]._direction
            return asteroids 
        else:
            return []

    def breakupshp(self,velocity,facing):
        """
        This method returns a list of new asteroids that are generated after a 
        collision with a ship.

        Parameter velocity: the ship's velocity at the moment of collision.
        Precondition: velocity is a valid ship velocity.
        Parameter facing: the ship's facing at the moment of collision.
        Precondition: facing is a valid ship facing.
        """
        radii=[SMALL_RADIUS,MEDIUM_RADIUS,LARGE_RADIUS]
        images=[SMALL_IMAGE,MEDIUM_IMAGE,LARGE_IMAGE]
        speeds=[SMALL_SPEED,MEDIUM_SPEED,LARGE_SPEED]
        if velocity.length()!=0:
            cv=velocity.normalize()
        else:
            cv=facing
        if self.width/2!=radii[0]:
            rad=radii[radii.index(self.width/2)-1]
            img=images[radii.index(self.width/2)-1]
            speed=speeds[radii.index(self.width/2)-1]
            new1=Vector2(self.x,self.y)+cv*rad
            cv2=cv.rotation(math.pi*2/3)
            new2=Vector2(self.x,self.y)+cv2*rad
            cv3=cv.rotation(-math.pi*2/3)
            new3=Vector2(self.x,self.y)+cv3*rad
            asteroids=[Asteroid(new1.x,new1.y,rad*2,rad*2,img,cv),
                Asteroid(new2.x,new2.y,rad*2,rad*2,img,cv2),
                Asteroid(new3.x,new3.y,rad*2,rad*2,img,cv3)]
            for i in range(len(asteroids)):
                    asteroids[i]._velocity=speed*asteroids[i]._direction
            return asteroids 
        else:
            return []
       

# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE


        

        
    
        








        

