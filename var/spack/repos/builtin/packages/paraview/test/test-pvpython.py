import paraview.simple
from paraview.simple import (
    ColorBy,
    GetActiveViewOrCreate,
    GetColorTransferFunction,
    GetLayout,
    GetMaterialLibrary,
    GetOpacityTransferFunction,
    GetTransferFunction2D,
    SaveScreenshot,
    Show,
    Sphere,
)

paraview.simple._DisableFirstRenderCameraReset()

# create a new "Sphere"
sphere1 = Sphere(registrationName="Sphere1")

# Properties modified on sphere1
sphere1.ThetaResolution = 32
sphere1.PhiResolution = 32

# get active view
renderView1 = GetActiveViewOrCreate("RenderView")

# show data in view
sphere1Display = Show(sphere1, renderView1, "GeometryRepresentation")

# trace defaults for the display properties.
sphere1Display.Representation = "Surface"
sphere1Display.ColorArrayName = [None, ""]
sphere1Display.SelectTCoordArray = "None"
sphere1Display.SelectNormalArray = "Normals"
sphere1Display.SelectTangentArray = "None"
sphere1Display.OSPRayScaleArray = "Normals"
sphere1Display.OSPRayScaleFunction = "PiecewiseFunction"
sphere1Display.SelectOrientationVectors = "None"
sphere1Display.ScaleFactor = 0.1
sphere1Display.SelectScaleArray = "None"
sphere1Display.GlyphType = "Arrow"
sphere1Display.GlyphTableIndexArray = "None"
sphere1Display.GaussianRadius = 0.005
sphere1Display.SetScaleArray = ["POINTS", "Normals"]
sphere1Display.ScaleTransferFunction = "PiecewiseFunction"
sphere1Display.OpacityArray = ["POINTS", "Normals"]
sphere1Display.OpacityTransferFunction = "PiecewiseFunction"
sphere1Display.DataAxesGrid = "GridAxesRepresentation"
sphere1Display.PolarAxes = "PolarAxesRepresentation"
sphere1Display.SelectInputVectors = ["POINTS", "Normals"]
sphere1Display.WriteLog = ""

# init the "PiecewiseFunction" selected for "ScaleTransferFunction"
sphere1Display.ScaleTransferFunction.Points = [
    -0.9987165331840515,
    0.0,
    0.5,
    0.0,
    0.9987165331840515,
    1.0,
    0.5,
    0.0,
]

# init the "PiecewiseFunction" selected for "OpacityTransferFunction"
sphere1Display.OpacityTransferFunction.Points = [
    -0.9987165331840515,
    0.0,
    0.5,
    0.0,
    0.9987165331840515,
    1.0,
    0.5,
    0.0,
]

# reset view to fit data
renderView1.ResetCamera(False)

# get the material library
materialLibrary1 = GetMaterialLibrary()

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(sphere1Display, ("POINTS", "Normals", "Magnitude"))

# rescale color and/or opacity maps used to include current data range
sphere1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
sphere1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for "Normals"
normalsLUT = GetColorTransferFunction("Normals")

# get opacity transfer function/opacity map for "Normals"
normalsPWF = GetOpacityTransferFunction("Normals")

# get 2D transfer function for "Normals"
normalsTF2D = GetTransferFunction2D("Normals")

# get layout
layout1 = GetLayout()

# layout/tab size in pixels
layout1.SetSize(1988, 1176)

# current camera placement for renderView1
renderView1.CameraPosition = [0.0, 0.0, 3.3432027854673882]
renderView1.CameraParallelScale = 0.8652845525187569

# save screenshot
SaveScreenshot("test-pvpython.png", renderView1, ImageResolution=[1988, 1176])
