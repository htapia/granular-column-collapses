#!/usr/bin/pvpython

import sys
from paraview.simple import *

if not globals().has_key("argv"): argv = sys.argv
# dist = []
# use paraview vtk class to construct the shape of deposit


# def getArea( Source ):
# 	a1 = IntegrateVariables( Source )
# 	a2 = a1.GetCellDataInformation().GetArray("Area")
# 	a3 = a2.GetRange()[0]
# 	return a3

# def getLength( Source ):
# 	a1 = IntegrateVariables( Source )
# 	a2 = a1.GetCellDataInformation().GetArray("Length")
# 	a3 = a2.GetRange()[0]
# 	return a3

def shapeDeposit(state):
    # dist = []
    # use paraview vtk class to construct the shape of deposit
    reader = LegacyVTKReader( FileNames=state )
    Grains = Glyph( GlyphType="2D Glyph", GlyphTransform="Transform2" )
    Grains.SetScaleFactor = 2.0
    Grains.ScaleMode = 'scalar'
    Grains.GlyphType.GlyphType = 'Circle'

    PythonCalculator1 = PythonCalculator(ArrayName='ys minus 4 times mean radius',
        Expression = 'inputs[0].Points[:,1]-4*mean(radius)')
    Calculator1 = Calculator(AttributeMode = 'Point Data',
        ResultArrayName = 'ygt4mr', Function = 'ys minus 4 times mean radius>0')
    Threshold2 = Threshold()
    Threshold2.ThresholdRange = [1.0, 10000.0]
    Threshold2.Scalars = ['POINTS', 'ygt4mr']
    Show()
    Delaunay2D2 = Delaunay2D()
    Delaunay2D2.Alpha = 0.01
    Show()
    FeatureEdges1 = FeatureEdges()
    Show()

    SetActiveSource(Threshold2)
    PythonCalculator5 = PythonCalculator()
    PythonCalculator5.ArrayName = 'nVel'
    PythonCalculator5.Expression = 'inputs[0].PointData[2]'
    Show()
    Calculator2 = Calculator()
    Calculator2.Function = 'mag(nVel)<0.01'
    Calculator2.ResultArrayName = 'nSpeed'
    Calculator2.AttributeMode = 'Point Data'
    Threshold3 = Threshold()
    Threshold3.Scalars = ['POINTS', 'nSpeed']
    Threshold3.ThresholdRange = [1.0, 10000.0]
    Delaunay2D4 = Delaunay2D()
    Delaunay2D4.Alpha = 0.01
    Show()
    FeatureEdges2 = FeatureEdges( Delaunay2D4 )
    Show( )
    
    csv_state = state.replace('collapse','static_deposit').replace('vtk','csv')
    print csv_state
    writer1 = CreateWriter(csv_state, FeatureEdges2)
    writer1.WriteAllTimeSteps = 0
    writer1.FieldAssociation = "Points"
    writer1.UpdatePipeline()
    del writer1

    csv_state = state.replace('vtk','csv')
    print csv_state
    writer2 = CreateWriter(csv_state, FeatureEdges1)
    writer2.WriteAllTimeSteps = 0
    writer2.FieldAssociation = "Points"
    writer2.UpdatePipeline()
    del writer2


filename = argv[1]

shapeDeposit( filename )

# colorStaticDeposit = GetDisplayProperties(FeatureEdges2)
# colorStaticDeposit.ColorArrayName = ('POINT_DATA', '')
# colorStaticDeposit.DiffuseColor= [1.0, 0.0, 0.0]
# Show( )


# # Calculate approx area
# areaDeposit = IntegrateVariables( Delaunay2D1 )
# areaDepositValue = areaDeposit.GetCellDataInformation().GetArray("Area")
# AreaDeposit = areaDepositValue.GetRange()[0]

# areaStaticDeposit = IntegrateVariables( Delaunay2D2 )
# areaStaticDepositValue = areaStaticDeposit.GetCellDataInformation().GetArray("Area")
# AreaStaticDeposit = areaStaticDepositValue.GetRange()[0]

# # Calculate approx perimeter
# perimeterDeposit = IntegrateVariables( FeatureEdges1 )
# perimeterDepositValue = perimeterDeposit.GetCellDataInformation().GetArray("Length")
# PerimeterDeposit = perimeterDepositValue.GetRange()[0]

# perimeterStaticDeposit = IntegrateVariables( FeatureEdges2 )
# perimeterStaticDepositValue = perimeterStaticDeposit.GetCellDataInformation().GetArray("Length")
# PerimeterStaticDeposit = perimeterStaticDepositValue.GetRange()[0]


# # return these numbers too
# print 'Full Deposit length: %0.3f; Static Deposit length: %0.3f'%(AreaDeposit, AreaStaticDeposit)

# print 'Full Deposit area: %0.3f; Static Deposit area: %0.3f'%(PerimeterDeposit, PerimeterStaticDeposit)

# vtkData = reader.GetClientSideObject()
# vtkData = vtkData.GetOutput()