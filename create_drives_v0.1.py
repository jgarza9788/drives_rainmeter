
import os

from drivedata import get_drivedata
DIR = os.path.dirname(os.path.realpath(__file__))

rainmeter = """

[Rainmeter]
Update=60
AccurateText=1
DynamicWindowSize=1

;https://forum.rainmeter.net/viewtopic.php?f=18&t=23106
;https://github.com/TheAzack9/FrostedGlass
[FrostedGlass]
Measure=Plugin
Plugin=FrostedGlass
Type=Blur
;Border=All
"""

variables = """

[variables]
RECSHAPE = 25,25,400,50,10
;BACKGROUNDCOLOR = 0,0,0,225
BACKGROUNDCOLOR = 0,0,0,175
LITECOLOR = "255,255,255,128"

NORMALCOLOR = "255,255,255,255"
; NORMALCOLOR = "0,0,0,255"
;HOVERCOLOR = "88,209,235,255" 
HOVERCOLOR = "0,0,0,255" 

FONTCOLOR = "255,255,255,125"
FONTCOLORHOVER = "255,255,255,255"

;ACTIVESHAPE="Rectangle 0,0,780,40,10 | Fill Color 152,224,36,255 | StrokeWidth 0 | Stroke Color 0,0,0,0"
; ACTIVESHAPE="Rectangle 0,0,380,120,5 | Fill Color 88,209,235,255 | StrokeWidth 0 | Stroke Color 0,0,0,0"
ACTIVESHAPE="Rectangle 0,0,425,80,0 | Fill Color 0,0,0,255 | StrokeWidth 0 | Stroke Color 0,0,0,0"
INACTIVESHAPE="Rectangle 0,0,425,80,0 | Fill Color 0,0,0,0 | StrokeWidth 0"

"""

startshapes = """

[background]
Meter=Shape
Shape=Rectangle 0,0,425,{height},0 | Fill Color #BACKGROUNDCOLOR# | StrokeWidth 0

[RefreshBtn]
Meter=String
;FontFace=Hack NF
FontFace=RobotoMono Nerd Font
FontSize=12
FontColor=#FONTCOLOR#
SolidColor=47,47,47,1
Padding=0,0,0,0
AntiAlias=1
Y=5r
X=16r
Text=""
MouseOverAction=[!SetOption RefreshBtn FontColor #FONTCOLORHOVER#][!UpdateMeter RefreshBtn][!Redraw]
MouseLeaveAction=[!SetOption RefreshBtn FontColor #FONTCOLOR#][!UpdateMeter RefreshBtn][!Redraw]
LeftMouseUpAction=["{path}"]

[anchor]
Meter=Shape
Shape=Rectangle 0,0,10,10,0 | Fill Color 0,0,0,0 | StrokeWidth 0
X=20
Y=30

"""


metertext = """

[DriveItem{index}]
Meter=Shape
Shape=#INACTIVESHAPE#
Y=0r
X=0
MouseOverAction=[!SetOption DriveItem{index} Shape "#ACTIVESHAPE#"][!SetOption Text{index}0 FontColor "#FONTCOLORHOVER#"][!SetOption Text{index}1 FontColor "#FONTCOLORHOVER#"][!SetOption Text{index}2 FontColor "#FONTCOLORHOVER#"][!UpdateMeter DriveItem{index}][!UpdateMeter Text{index}0][!UpdateMeter Text{index}1][!UpdateMeter Text{index}2][!Redraw]
MouseLeaveAction=[!SetOption DriveItem{index} Shape "#INACTIVESHAPE#"][!SetOption Text{index}0 FontColor "#FONTCOLOR#"][!SetOption Text{index}1 FontColor "#FONTCOLOR#"][!SetOption Text{index}2 FontColor "#FONTCOLOR#"][!UpdateMeter DriveItem{index}][!UpdateMeter Text{index}0][!UpdateMeter Text{index}1][!UpdateMeter Text{index}2][!Redraw]
LeftMouseUpAction=["{drive}"]

[Text{index}0]
Meter=String
FontFace=RobotoMono Nerd Font
FontSize=12
FontColor=#FONTCOLOR#
SolidColor=47,47,47,0
Padding=0,0,0,0
AntiAlias=1
Y=6r
X=10r
StringAlign=Left
Text="󰋊 {drive} {drive_name}"

[Text{index}1]
Meter=String
FontFace=RobotoMono Nerd Font
FontSize=12
FontColor=#FONTCOLOR#
SolidColor=47,47,47,0
Padding=0,0,0,0
AntiAlias=1
Y=24r
X=0r
StringAlign=Left
Text="{capacity_string}"

[Text{index}2]
Meter=String
FontFace=RobotoMono Nerd Font
FontSize=12
FontColor=#FONTCOLOR#
SolidColor=47,47,47,0
Padding=0,0,0,0
AntiAlias=1
Y=24r
X=0r
StringAlign=Left
Text="{bar}"

[anchor{index}]
Meter=Shape
Shape=Rectangle 0,0,10,10,0 | Fill Color 0,0,0,0 | StrokeWidth 0
X=0r
Y=27r

"""


def save(contents, file_path):
    """saves the rainmeter .ini file

    Args:
        text (str): contents of the file
        file_path (str): location to save the file
    """
    with open(file_path,'w',encoding="utf-16") as f:
        f.write(contents)

def bar(num,denom,length=50,fillchar='#',emptychar=' '):
    fillnum = ((int)( (num/denom) * length))
    return '[' + ( fillnum * fillchar ).ljust(length,emptychar)  + ']'


def main():
    dd = get_drivedata()

    rm = rainmeter
    rm += variables
    rm += startshapes.format(
        height=(60 + ( len(dd) * 80 )  ),
        path = r'C:\Users\JGarza\Documents\Rainmeter\Skins\drives\mr'
        )

    for i,d in enumerate(dd):  
        mt = metertext.format(
            index = str(i),
            drive = d['letter'] + '\\',
            drive_name = d.get('volumename',''),
            capacity_string = "{0:.2f} / {1:.2f} | {2} %".format( d['used_round'] , d['size'] , d['percent_used'] ),
            bar= bar(d['percent_used'],100.0,length=40,emptychar='.')
        )

        rm += mt
    

    
    save(rm,os.path.join(DIR,'drives.ini'))



if __name__ == "__main__":

    main()

