Set pna = CreateObject("AgilentPNA835x.Application")
Set calMgr = pna.GetCalManager
Set guidedCal = calMgr.GuidedCalibration
Set chan = pna.ActiveChannel
chanNum = chan.ChannelNumber
' Initialize guided cal to be performed on the active channel.
' The boolean argument of True indicates to create a new calset
guidedCal.Initialize chanNum, True
' Do 1-port cal
OnePortGuidedCal
' Do 2-port cal
'TwoPortGuidedCal
' Do 3-port cal
'ThreePortGuidedCal


Sub OnePortGuidedCal()
' Cambia el conector según tu ECal
guidedCal.ConnectorType(1) = "APC 2.92 male "
For i = 2 To pna.NumberOfPorts
    guidedCal.ConnectorType(i) = "Not used"
Next
value = MsgBox("Conector definido para el Puerto 1")
' Selecciona el ECal para el puerto calibrado
guidedCal.CalKitType(1) = "N4692-60001 ECal"
' Si tienes más puertos, ignóralos
For i = 2 To pna.NumberOfPorts
    guidedCal.CalKitType(i) = ""
Next
MsgBox("Cal kit definido para el Puerto 1")
' Inicia la calibración
numSteps = guidedCal.GenerateSteps
' Mide los estándares, calcula y aplica la calibración
MeasureAndComplete(numSteps)
End Sub


Sub TwoPortGuidedCal()
'Change the following to match the connectors on your ECal module
guidedCal.ConnectorType(1) = "APC 3.5 female"
guidedCal.ConnectorType(2) = "APC 3.5 female"
For i = 3 To pna.NumberOfPorts
guidedCal.ConnectorType(i) = "Not used"
Next
value = MsgBox("Connectors defined for Ports 1 and 2")
' Select the ECal module for each port being calibrated.
guidedCal.CalKitType(1) = "N4691-60004 ECal"
guidedCal.CalKitType(2) = "N4691-60004 ECal"
MsgBox("Cal kits defined for Ports 1 and 2")
numSteps = guidedCal.GenerateSteps
MeasureAndComplete(numSteps)
End Sub


Sub ThreePortGuidedCal()
guidedCal.ConnectorType(1) = "APC 3.5 female"
guidedCal.ConnectorType(2) = "APC 3.5 female"
guidedCal.ConnectorType(3) = "APC 3.5 female"
guidedCal.CalKitType(1) = "N4431-60003 ECal"
guidedCal.CalKitType(2) = "N4431-60003 ECal"
guidedCal.CalKitType(3) = "N4431-60003 ECal"
value = MsgBox("Cal kits defined for Ports 1 to 3")
numSteps = guidedCal.GenerateSteps
MeasureAndComplete(numSteps)
End Sub

Sub MeasureAndComplete(ByVal numSteps)
value = MsgBox("Number of steps is " + CStr(numSteps))
For i = 1 To numSteps
step = "Step " + CStr(i) + " of " + CStr(numSteps)
strPrompt = guidedCal.GetStepDescription(i)
value = MsgBox(strPrompt, vbOKOnly, step)
guidedCal.AcquireStep i
Next
guidedCal.GenerateErrorTerms
MsgBox ("Cal is done!")
End Sub