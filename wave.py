"""
Subcontroller module for Planetoids

This module contains the subcontroller to manage a single level (or wave) in the 
Planetoids game.  Instances of Wave represent a single level, and should correspond
to a JSON file in the Data directory. Whenever you move to a new level, you are 
expected to make a new instance of the class.

The subcontroller Wave manages the ship, the asteroids, and any bullets on screen. These 
are model objects. Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Ed Discussions and we will answer.

# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""
from game2d import *
from consts import *
from models import *
import random
import datetime

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Level is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)

class Wave(object):
    """
    This class controls a single level or wave of Planetoids.
    
    This subcontroller has a reference to the ship, asteroids, and any bullets on screen.
    It animates all of these by adding the velocity to the position at each step. It
    checks for collisions between bullets and asteroids or asteroids and the ship 
    (asteroids can safely pass through each other). A bullet collision either breaks
    up or removes a asteroid. A ship collision kills the player. 
    
    The player wins once all asteroids are destroyed.  The player loses if they run out
    of lives. When the wave is complete, you should create a NEW instance of Wave 
    (in Planetoids) if you want to make a new wave of asteroids.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lecture 25 for an example.  This class will be similar to
    than one in many ways.
    
    All attributes of this class are to be hidden. No attribute should be accessed 
    without going through a getter/setter first. However, just because you have an
    attribute does not mean that you have to have a getter for it. For example, the
    Planetoids app probably never needs to access the attribute for the bullets, so 
    there is no need for a getter there. But at a minimum, you need getters indicating
    whether you one or lost the game.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # THE ATTRIBUTES LISTED ARE SUGGESTIONS ONLY AND CAN BE CHANGED AS YOU SEE FIT
    # Attribute _data: The data from the wave JSON, for reloading 
    # Invariant: _data is a dict loaded from a JSON file
    #
    # Attribute _ship: The player ship to control 
    # Invariant: _ship is a Ship object
    #
    # Attribute _asteroids: the asteroids on screen 
    # Invariant: _asteroids is a list of Asteroid, possibly empty
    #
    # Attribute _bullets: the bullets currently on screen 
    # Invariant: _bullets is a list of Bullet, possibly empty
    #
    # Attribute _lives: the number of lives left 
    # Invariant: _lives is an int >= 0
    #
    # Attribute _firerate: the number of frames until the player can fire again 
    # Invariant: _firerate is an int >= 0
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getLives(self):
        """
        Returns the number of lives left for the given wave, i.e.
        returns the lives attribute."""
        return self._lives

    def setLives(self,lives):
        """
        Sets lives attribute to lives.
        Parameter lives: the lives to set to
        Precondition: lives is an integer in the range from 0 to 
        SHIP_LIVES, inclusive
        """
        self._lives=lives

    def setAsteroidsvelocity(self,velocity):
        """ 
        Sets the velocity of each asteroid in the wave to a given velocity.

        Parameter velocity: the velocity to set to.
        Precondition: velocity is a list of velocity x and y coordinates.
        """
        for i in range(len(self._asteroids)):
            self._asteroids[i].setVelocity(velocity)
    
    # INITIALIZER (standard form) TO CREATE SHIP AND ASTEROIDS
    def __init__(self,json):
        """Creates a Wave.

        The wave is created from the data stored in the json.              
        Paramater json: the level to load

        Precondition: json is a dictionary loaded from a JSON file
        """
        self._data=json                  
        xs=self._data['ship']['position'][0]
        ys=self._data['ship']['position'][1]
        sangle=self._data['ship']['angle']
        self._ship=Ship(xs,ys,sangle)
        self._asteroids=[]
        for item in self._data['asteroids']:
            size=item['size']
            xa=item['position'][0]
            ya=item['position'][1]
            direction=item['direction']
            dv=Vector2(direction[0],direction[1])
            sizes=[SMALL_ASTEROID,MEDIUM_ASTEROID,LARGE_ASTEROID]
            sources=[SMALL_IMAGE,MEDIUM_IMAGE,LARGE_IMAGE]
            radii=[SMALL_RADIUS,MEDIUM_RADIUS,LARGE_RADIUS]
            index=sizes.index(size)
            source=sources[index]
            width=radii[index]*2
            height=radii[index]*2
            self._asteroids.append(Asteroid(xa,ya,width,height,source,dv))    
        self._bullets=[]
        self._firerate=0               
        self._lives=SHIP_LIVES
    
    # UPDATE METHOD TO MOVE THE SHIP, ASTEROIDS, AND BULLETS
    def update(self,input,dt):
        """
        Animates the ship.                          
        
        Parameter input:the user input, used to control the ship and change state
        Precondition: input is an instance of GInput 
        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.
        """
        
        if self.getLives()!=0 or len(self._asteroids)!=0:      
            if self._ship!=None:
                self._ship.turnship(input)
                self._ship.x+=self._ship.getVelocity().x   
                self._ship.y+=self._ship.getVelocity().y    
                self._ship.wrapship()           
                self.asteroidwrapandvel()
                self.fire(input)
                self.deletebullet()
                self.resolve() 
        
    # DRAW METHOD TO DRAW THE SHIP, ASTEROIDS, AND BULLETS
    def draw(self,view):
        """
        This method draws the ship, asteroids and bullets.

        Parameter: The view window
        Precondition: view is a GView.
        """
        if self._ship!=None:
            self._ship.draw(view)
        for item in self._asteroids:
            item.draw(view)
        for item in self._bullets:
            item.draw(view)
    
    # RESET METHOD FOR CREATING A NEW LIFE
    def newship(self):
        """
        This method created a new ship after a life is lost.
        """
        xs=self._data['ship']['position'][0]
        ys=self._data['ship']['position'][1]
        sangle=self._data['ship']['angle']
        self._ship=Ship(xs,ys,sangle)
        
    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION
    def isshipnone(self):
        """
        This method returns True if ship is None, False otherwise.
        """
        if self._ship==None:
            return True
        else:
            return False

    def win(self):
        """
        This method returns True if no asteroids left on the screen.
        Returns False otherwise.
        """
        if self._asteroids==[]:
            return True
        else:
            return False
    
    def asteroidwrapandvel(self):
        """
        This method wraps each asteroid and changes its position according 
        to the velocity.
        """
        for i in range(len(self._asteroids)):
            self._asteroids[i].x+=self._asteroids[i].getVelocity().x
            self._asteroids[i].y+=self._asteroids[i].getVelocity().y
            self._asteroids[i].wrapasteroid()

    def fire(self,input):
        """
        This method checks for input 'spacebar' and creates apends the created 
        bullet to the bullet list. It then changes the positions of the bullets 
        according to the velocities.

        Parameter input:the user input, used to control the ship and change state
        Precondition: input is an instance of GInput
        """
        if input.is_key_down('spacebar') and self._firerate>=BULLET_RATE:                   
            x=self._ship.getFacing().x*SHIP_RADIUS+self._ship.x
            y=self._ship.getFacing().y*SHIP_RADIUS+self._ship.y
            width=BULLET_RADIUS*2
            height=BULLET_RADIUS*2
            self._bullets.append(Bullet(self._ship.getFacing(),x,y,width,height))
            self._firerate=0            
        self._firerate+=1               
        for i in range(len(self._bullets)):
            self._bullets[i].x+=self._bullets[i].getVelocity().x
            self._bullets[i].y+=self._bullets[i].getVelocity().y

    def deletebullet(self):
        """
        This method deletes the given bullet from the list of bullets when it 
        exists the window.
        """
        i=0
        while i<len(self._bullets):
            if GAME_WIDTH+2*DEAD_ZONE<self._bullets[i].x<-DEAD_ZONE:
                del self._bullets[i]
            else:
                i+=1   

    def resolve(self):
        """
        This method resolves collisions: asteroid and ship or asteroid and bullet.
        It breaks up the asteroids when hit by a bullet

        """
        self.detect()
        self.cleanup()

    def detect(self):
        """
        This method detects collisions: either between asteroid and ship or 
        asteroid and bullet. It also breaks up the asteroids as needed and sets 
        the ship to none as needed. 
        """
        if self._ship!=None:
            length=len(self._asteroids)
            for i in range(length):
                if self._ship!=None:
                    positions=self._ship.getPosition()
                    if (self._asteroids[i]!=None and self._ship!=None
                        and self._asteroids[i].collideshp(positions)):
                        velocitys=self._ship.getVelocity()
                        facing=self._ship.getFacing()
                        self._asteroids[i].setDeleted(True)
                        self._asteroids+=self._asteroids[i].breakupshp(velocitys,
                            facing)
                        self._ship=None
                    for k in range(len(self._bullets)):
                        positionb=self._bullets[k].getPosition()
                        if (self._asteroids[i]!=None and self._bullets[k]!=None 
                            and self._asteroids[i].collideshp(positionb)):
                            velocityb=self._bullets[k].getVelocity()
                            self._asteroids+=(
                                self._asteroids[i].breakupblt(velocityb))       
                            self._asteroids[i].setDeleted(True)
                            self._bullets[k].setDeleted(True)
        
    def cleanup(self):
        """
        Removes collided items from their lists.
        """   
        i=0
        while i<len(self._asteroids):
            if self._asteroids[i].getDeleted():
                del self._asteroids[i]
                
            else:
                i+=1
        k=0
        while k<len(self._bullets):
            if self._bullets[k].getDeleted():
                del self._bullets[k]
            else:
                k+=1

    






