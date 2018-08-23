B4J=true
Group=Models
ModulesStructureVersion=1
Type=Class
Version=5.9
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
		'[Loteamentos.Id <1N> Lotes.LoteamentoId]
		Private Lotes_ As List
	'</Relationships>

	Private fx As JFX
End Sub


Public Sub Initialize()

End Sub

Public Sub ToString() As String
	Dim sb As StringBuilder
	sb.Initialize
	sb.Append("Id=" & Id & ", ")
	sb.Append("Nome=" & Nome & ", ")
	sb.Append("Cidade=" & Cidade & ", ")
	sb.Append("Numlotes=" & Numlotes & ", ")
	sb.Remove(sb.Length - 2, sb.Length)
	Return sb.ToString
End Sub

#Region RELASHIONSHIPS

Public Sub getLotes As List
	If Lotes_.IsInitialized Then
		Return Lotes_
	Else
		Dim da As DBDadosDataAccess
		da.initialize
		Lotes_ = da.Lotes_Where2("LoteamentoId=?", Array(Id))
		da.Dispose
		Return Lotes_
	End If
End Sub

#End Region
