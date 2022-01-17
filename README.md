# visiview-scripts
A collection of macros for the VisiView acquisition software

## Installation
Copy whole folder to ``C:\ProgramData\Visitron Systems\VisiView\PythonMacros\FMI-git``
Configure the default toolbar to include
loadTileImageToolbar


## Usage
Acquire one or multiple color (no Z-stack) tiled image


Draw one or more region on the overlay image. For more regions click on the icon top-left.

Save Regions

If you want a focus map you change Stage Positions and label points where the focus map will be computed.
A good strategy is to mark the top or bottom of the sample and then always acquire a certain number of planes from this positions. 


Acquire Multiple Tiled Regions 
 


## Questions
Simple ScanSlice with Z-Stack makes a maximal projection of XYZC image but the resulting image can' t be used to navigate. There is no calibration 
associated to it so it is just for a quick overview.
May be we can ask Visitron to provide a function for association calibration to an image. This is done with the Overview image. 

What are GetPlateStartPositions, etc. Is this to reorient on larger slides and rerun the aquisition?


