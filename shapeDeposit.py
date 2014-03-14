#!/usr/bin/pvpython

import sys
from paraview.simple import *

if not globals().has_key("argv"): argv = sys.argv

# returns the deposit from vtk data#####################################################################################################

def shapeDeposit(state):
    dist = []
    # use paraview vtk class to construct the shape of deposit
    reader = LegacyVTKReader( FileNames=state )
    # DepositProfile
    Grains = Glyph( GlyphType="2D Glyph", GlyphTransform="Transform2" )
    Grains.SetScaleFactor = 2.0
    Grains.ScaleMode = 'scalar'
    Grains.GlyphType.GlyphType = 'Circle'
    # calculate stuff needed to find the pile shape
    PythonCalculator1 = PythonCalculator(ArrayName='ys minus 4 times mean radius',
        Expression = 'inputs[0].Points[:,1]-4*mean(radius)')
    Calculator1 = Calculator(AttributeMode = 'Point Data',
        ResultArrayName = 'ygt4mr', Function = 'ys minus 4 times mean radius>0')
    ClipDeposit = Clip( ClipType="Scalar", Scalars = ['POINTS', 'ygt4mr'] )
    Delaunay2D1 = Delaunay2D( Alpha=0.01 )
    FeatureEdges1 = FeatureEdges( )
    Show()

    vtkData = reader.GetClientSideObject()
    vtkData = vtkData.GetOutput()

    return FeatureEdges1, vtkData #xm_l,xm_r,hm

#####################################################################################################

filename = argv[1]

depositProfile = shapeDeposit( filename )


