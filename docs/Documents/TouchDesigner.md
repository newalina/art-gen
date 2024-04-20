# First
## OPerators === Nodes
> TouchDesigner Operators are [[#Generators]] or [[#Filters]]. "Filters" require at least one input, and modify the data of an incoming operator.

> Each operator is customized with its [Parameters](https://derivative.ca/UserGuide/Parameter "Parameter") and [Flags](https://derivative.ca/UserGuide/Flag "Flag").

### Generators
> Create or Read ext. data
>	Ex) a Video.mp4 "generates" many Image.png[]
>Dark colored

### Filters
> Modify output data of an Input OP
> Light colored


## OPerator Families

The [OP Create Dialog](https://derivative.ca/UserGuide/OP_Create_Dialog "OP Create Dialog") has six headings of what we call [Operator Families](https://derivative.ca/UserGuide/Operator "Operator"). Click on '[CHOP](https://derivative.ca/UserGuide/CHOP "CHOP")' for 'Channel Operators'. Press Tab several times to cycle back to CHOPs.

TextureOP

Click on the CHOP type "Pattern" and place the Pattern CHOP in the network in a row above the TOPs. Channel Operators are used for motion, control signals, audio and more.

Bring up OP Create again. You can find a specific operator by typing its name. Type "noi", click on Noise, and before clicking again, you can use the roller wheel to zoom the network and find a space, and click to create a [Noise CHOP](https://derivative.ca/UserGuide/Noise_CHOP "Noise CHOP").

Bring up OP Create and Click "SOP". Surface Operators ([SOPs](https://derivative.ca/UserGuide/SOP "SOP")) work with polygons, 3D lines and other surfaces. Choose a [Sphere SOP](https://derivative.ca/UserGuide/Sphere_SOP "Sphere SOP") and place the node in the network.

Press the Tab key and select "MAT". Material Operators ([MATs](https://derivative.ca/UserGuide/MAT "MAT")) add textures and shading to 3D objects. Choose a [Phong MAT](https://derivative.ca/UserGuide/Phong_MAT "Phong MAT") and place the node.

Press the Tab key and select "DAT". Data Operators ([DATs](https://derivative.ca/UserGuide/DAT "DAT")) manipulate text strings, both free-form text and in tables. Choose a [Monitors DAT](https://derivative.ca/UserGuide/Monitors_DAT "Monitors DAT"), which is a table containing one row for every monitor attached to your computer.


## COMPonents
Press the Tab key and select "COMP" for Components. There are four categories of components. From the 3D Objects column on the left, choose a [Geometry COMP](https://derivative.ca/UserGuide/Geometry_COMP "Geometry COMP"), which unites SOPs and a Material for 3D rendering.

Press the Tab key again. From the Panels column, choose a [Slider COMP](https://derivative.ca/UserGuide/Slider_COMP "Slider COMP"), which is one of the 2D gadgets for building control panels.

>The 3D components like Geometrys, Cameras and Lights have connectors on their bottoms and tops (connect them) which connects them as **parent-child in a [3D](https://derivative.ca/UserGuide/3D "3D") hierarchy, but no data flows along them.**

## Parameters (for an OP)
> Every Operator in TouchDesigner has a set of [Parameters](https://derivative.ca/UserGuide/Parameter "Parameter") that affects its output.

→ ** *we*  supply OPs, they specify Parameters and can save multiple configurations **
--- 
# COOK
> When a wire is animating it means that data is flowing: the node upstream is [cooking](https://derivative.ca/UserGuide/Cook "Cook") and giving its output to the next node to cook, and so on downstream.