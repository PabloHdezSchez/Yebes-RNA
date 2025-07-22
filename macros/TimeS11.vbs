' filepath: /home/oanuser/PabloH/Analizador/macros/TimeS11.vbs
' Script para Keysight PNA N5227B - Medida S11 en dominio temporal usando SCPI y VBScript

Dim app
Dim scpi

' Crear / Obtener la aplicación del VNA
Set app = CreateObject("AgilentPNA835x.Application")
Set scpi = app.ScpiStringParser

' Preset del analizador (borra configuraciones previas)
scpi.Execute("SYST:FPReset")

' Crear y activar la ventana 1
scpi.Execute("DISP:WIND1:STAT ON")

' Ajuste del filtro paso bajo
scpi.Execute("CALC:MATH:TDOM:MODE LOWPASS_STEP")

' Ajuste del factor de velocidad
scpi.Execute("CALC:MATH:TDOM:VFAC 0.7")

' Definir la medida S11 con nombre 'MyMeas'
scpi.Execute("CALC:PAR:DEF:EXT 'MyMeas', 'S11'")

' Asociar la medida a la ventana y traza 1
scpi.Execute("DISP:WIND1:TRAC1:FEED 'MyMeas'")

' Ajustes de dominio temporal
scpi.Execute("CALC:MATH:TDOM:STAT ON")
scpi.Execute("CALC:MATH:TDOM:STAR 0")
scpi.Execute("CALC:MATH:TDOM:STOP 2E-9")
scpi.Execute("CALC:MATH:TDOM:TRAN ON")

' Formato de representación REAL
scpi.Execute("CALC:FORM REAL")

' Autoscale para visualizar correctamente
scpi.Execute("DISP:WIND1:Y:AUTO")

' Fin del script