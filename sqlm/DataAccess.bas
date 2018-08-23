B4J=true
Group=Controllers
ModulesStructureVersion=1
Type=Class
Version=6.0
@EndOfDesignText@
Sub Class_Globals
	Private fx as JFX
	Private SQL1 As SQL
End Sub

Public Sub initialize
	SQL1.InitializeSQLite(File.DirApp, ".db", True)
End Sub
Public Sub Dispose
	SQL1.Close
End Sub

Public Sub getSQL As SQL
	Return SQL1
End Sub

