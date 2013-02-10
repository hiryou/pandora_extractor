__author__="longuyen"
__date__ ="$8-Feb-2013 3:29:44 AM$"

from app.Welcome import Welcome
from app.FlowControl import FlowControl

if __name__ == '__main__':
    Welcome.disclaimer()
    control = FlowControl()
    control.start()
