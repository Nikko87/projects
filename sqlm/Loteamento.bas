B4J=true
Group=Models
ModulesStructureVersion=1
Type=Class
Version=6.3
@EndOfDesignText@
'[Table: Loteamentos]
'[Database: DBDados]
Sub Class_Globals
	'<Columns>
		Public Id As Int '[PrimaryKey, AutoIncrement]

		Public Nome As String '[NotNull]

		Public Cidade As String '[NotNull]

		Public Numlotes As Int '[NotNull]

		Public Teste1 As String '[]

	'</Columns>
	'<Relationships>
		Private Lotes_ As List '[Loteamentos.Id <1N> Lotes.LoteamentoId]

	'</Relationships>
End Sub
Public Sub Initialize

End Sub
#Region Relationships
'Loteamentos.Id <1N> Lotes.LoteamentoId
Public Sub getLotes As List
	If Lotes_.IsInitialized then
		Return Lotes_
	Else
		Dim da As DBDadosDataAccess
		da.Initialize
		Lotes_ = da.Lotes_Where2("LoteamentoId=?", Array(Id))
		da.Dispose
		Return Lotes_
	End If
End Sub
#End Region

#Region Subs
	'Write here the subs you want to save
#End Region


#Region Subs
	'Write here the subs you want to save
#End Region

