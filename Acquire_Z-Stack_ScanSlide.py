# VisiView Macro
import sys
sys.path.append(r"C:\ProgramData\Visitron Systems\VisiView\PythonMacros\Examples\Image Access\OpenCV\Library")
vvimport('OpenCV')

def acquire(xTiles, yTiles,  xPixels, yPixels, bin, cal, areaTopLeftX, areaTopLeftY, totalSizeX, totalSizeY, resultImages, overviewWindows):

	# loop through X and Y dimensions to acquire tiles
	for i in range(xTiles):
		for j in range(yTiles):
			VV.Stage.XPosition = areaTopLeftX + (0.5 * xPixels * bin * cal) + (i * xPixels * bin * cal * 0.9)
			VV.Stage.YPosition = areaTopLeftY + (0.5 * yPixels * bin * cal) + (j * yPixels * bin * cal * 0.9)
			VV.Macro.Control.Delay(500, "ms") # FIXME is this required?

			channelWindows = []
			baseName = VV.Acquire.Sequence.GetNextBaseNameFromStartNumber(1)

			# ***** ACQUISITION START *****
			VV.Acquire.Sequence.Start()

			if len(overviewWindows) > 1:
				# Get all aquisition windows as they appear
				for ch,_ in enumerate(overviewWindows):
					currentWindow = VV.Window.GetHandle.Empty
					while VV.Window.GetHandle.CheckIfEmpty(currentWindow):
						currentWindow = VV.Window.GetHandle.Acquire(ch+1)
					channelWindows.append(currentWindow)
					print currentWindow.Name

			VV.Macro.Control.WaitFor('VV.Acquire.IsRunning', "==", False)
			# ***** ACQUISITION END *****

			if len(overviewWindows) == 1:
				# Get single channel acquisition window
				list = VV.Window.GetHandle.List
				channelWindows.append(list[len(list)-1])

			# Select each channel, do MIP, add to respective resultImage
			for index, currentChannel in enumerate(channelWindows):
				VV.Window.Selected.Handle = currentChannel;
				MIP = VV.Process.StackArithmetic('StackMaximum','ProcessOverzfocus')

				# Create CvMat image of same dimensions
				tmpMIP = CvMat(yPixels, xPixels, MatrixType.U16C1)
				tmpCopy = CvMat(totalSizeY, totalSizeX, MatrixType.U16C1)
				VV.Image.ReadToPointer(tmpMIP.Data)
				VV.Window.Selected.Close(False)
				offset = CvPoint(i * xPixels*0.9, j * yPixels*0.9)
				tmpMIP.CopyMakeBorder(tmpCopy, offset, 0)
				resultImages[index].Max(tmpCopy, resultImages[index])

				VV.Window.Selected.Handle = currentChannel
				VV.Window.Selected.Close(False)

				VV.Window.Selected.Handle = overviewWindows[index]
				VV.Image.WriteFromPointer(resultImages[index].Data, totalSizeY, totalSizeX)

def main():
	# Initialize
	VV.Macro.PrintWindow.Clear()
	VV.Acquire.Stage.Series = False
	VV.Acquire.Sequence.SaveToDisk = True
	
	# Retrieve information about tile experiment
	areaTopLeftX = VV.Acquire.Stage.ScanSlide.Area.UpperLeft.X
	areaTopLeftY = VV.Acquire.Stage.ScanSlide.Area.UpperLeft.Y
	areaLowerRightX = VV.Acquire.Stage.ScanSlide.Area.LowerRight.X
	areaLowerRightY = VV.Acquire.Stage.ScanSlide.Area.LowerRight.Y

	# Retrieve information about frame and calibration
	xPixels = VV.Acquire.XDimension
	yPixels = VV.Acquire.YDimension
	bin = VV.Acquire.Binning
	cal = VV.Magnification.Calibration.Value

	# Calculate number of tiles	
	xTiles = int(round((areaLowerRightX-areaTopLeftX)/cal/bin/xPixels))
	yTiles = int(round((areaLowerRightY-areaTopLeftY)/cal/bin/yPixels))

	# Calculate size of final stitched image and display empty image
	totalSizeX = xPixels * 0.9 * xTiles + xPixels * 0.1
	totalSizeY = yPixels * 0.9 * yTiles + yPixels * 0.1

	# Get number of channels
	if VV.Acquire.WaveLength.Series:
		nChannels = VV.Acquire.WaveLength.Count
	else:
		nChannels = 1

	resultImages = []
	overviewWindows = []
	for c in range(nChannels):
		resultImage = CvMat(totalSizeY, totalSizeX, MatrixType.U16C1)
		resultImage.Set(CvScalar(0))
		overviewWindows.append(VV.Process.CreateEmptyPlane('Monochrome16', totalSizeX, totalSizeY))	
		VV.Image.WriteFromPointer(resultImage.Data, totalSizeY, totalSizeX)
		resultImages.append(resultImage)

	# Acquire tiles
	acquire(xTiles, yTiles, xPixels, yPixels, bin, cal, areaTopLeftX, areaTopLeftY, totalSizeX, totalSizeY, resultImages, overviewWindows)

	# Re-activate series option
	VV.Acquire.Stage.Series = True

try:
	main()
except KeyboardInterrupt:
	# Re-activate series option
	VV.Acquire.Stage.Series = True
