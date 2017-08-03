import ac, acsys
import platform, os, sys, math

if platform.architecture()[0] == "64bit":
	sysdir = os.path.dirname(__file__)+'/lib/x64'
else:
	sysdir = os.path.dirname(__file__)+'/lib/x86'

sys.path.insert(0, sysdir)
os.environ['PATH'] = os.environ['PATH'] + ";."

from lib.sim_info import info

import ctypes
from ctypes import wintypes

def acMain(ac_version):
    global windSpeed
    appWindow = ac.newApp("mWind")
    ac.setSize(appWindow,180,100)
    ac.drawBorder(appWindow,0)
    ac.setBackgroundOpacity(appWindow, 0)
    ac.setTitle(appWindow, "")
    ac.drawBorder(appWindow, 0)
    ac.setIconPosition(appWindow, 0, -10000)
    windSpeed = ac.addLabel(appWindow, "{:.1f} km/h".format(info.graphics.windSpeed));
    ac.setPosition(windSpeed, 90, 50)
    ac.addRenderCallback(appWindow , onFormRender)
    return "mWind"

def onFormRender(deltaT):
    global windSpeed
    ac.setText(windSpeed, "{:.1f} km/h".format(info.graphics.windSpeed))
    headingRad = info.physics.heading + 2 * math.pi if info.physics.heading < 0 else info.physics.heading
    headingDeg = (headingRad / (2 * math.pi)) * 360
    windHeading = info.graphics.windDirection + 180 if info.graphics.windDirection < 181 else info.graphics.windDirection - 180
    relativeWind = windHeading - headingDeg + 360 if headingDeg > windHeading else windHeading - headingDeg
    drawIndicator(relativeWind)

def drawVector(vector):
    ac.glVertex2f(vector['x'], vector['y'])

def calculateNewPoint(o, p, rotation):
    rotation = rotation * math.pi / 180
    cos = math.cos(rotation);
    sin = math.sin(rotation);
    wx = cos * (p['x']-o['x']) - sin * (p['y']-o['y']) + o['x']
    wy = sin * (p['x']-o['x']) + cos * (p['y']-o['y']) + o['y']
    return {'x': wx, 'y': wy}

def drawIndicator(degrees):
    radians = degrees * math.pi / 180
    cos = math.cos(radians);
    sin = math.sin(radians);
    # Center point
    o = {'x': 30, 'y': 60}
    # 0 degrees point
    p = {'x': 30, 'y': 30}
    # Wind point
    w = calculateNewPoint(o, p, degrees)

    a1 = calculateNewPoint(w, o, 20)
    a2 = calculateNewPoint(w, o, -20)

    ac.glColor4f(1, 1, 1, 1)

    if 0 < degrees <= 45 or 315 < degrees <= 360:
        ac.glColor4f(0.21, 0.75, 0.45, 1) # Green

    if 45 < degrees <= 135 or 225 < degrees <= 315:
        ac.glColor4f(0.84, 0.63, 0.09, 1) # Yellow

    if 135 < degrees <= 225:
        ac.glColor4f(0.75, 0.21, 0.23, 1) # Red

    ac.glBegin(acsys.GL.Triangles)
    drawVector(w)
    drawVector(a1)
    drawVector(a2)
    ac.glEnd()
    ac.glColor4f(1,1,1,1)
