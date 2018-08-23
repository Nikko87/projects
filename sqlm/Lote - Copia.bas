B4J=true
Group=Models
ModulesStructureVersion=1
Type=Class
Version=5.9
@EndOfDesignText@
'[Table: Lotes]
'[Database: DBDados]
Sub Class_Globals
	'<Columns>
		
		Public Id As Int '[PrimaryKey, AutoIncrement]
		
		Public LoteamentoId As Int '[ForeignKey(Loteamentos.Id)]
		
		Public Quadra As String '[NotNull]
		
		Public Lote As String '[NotNull]
		
		Public Area As Double '[]
		
		Public Preco As Double '[]
		
		Public Situacao As Int '[NotNull]
	'</Columns>

	'<Relationships>
		'[Lotes.Id <1N> Parcelas.LoteId]
		Private Parcelas_ As List
		'[Lotes.LoteamentoId <N1> Loteamentos.Id]
		Private Loteamento_ As Loteamento
		'[Lotes.Id <1N> Vendas.LoteId]
		Private Vendas_ As List
	'</Relationships>

	Private fx as JFX
End Sub


Public Sub Initialize()

End Sub

Public Sub ToString() As String
	Dim sb as StringBuilder
	sb.Initialize
	sb.Append("Id=" & Id & ", ")
	sb.Append("LoteamentoId=" & LoteamentoId & ", ")
	sb.Append("Quadra=" & Quadra & ", ")
	sb.Append("Lote=" & Lote & ", ")
	sb.Append("Area=" & Area & ", ")
	sb.Append("Preco=" & Preco & ", ")
	sb.Append("Situacao=" & Situacao & ", ")
	sb.Remove(sb.Length - 2, sb.Length)
	Return sb.ToString
End Sub

#Region RELASHIONSHIPS

Public Sub getParcelas As List
	If Parcelas_.IsInitialized Then
		Return Parcelas_
	Else
		Dim da As DBDadosDataAccess
		da.initialize
		Parcelas_ = da.Parcelas_Where2("LoteId=?", Array(Id))
		da.Dispose
		Return Parcelas_
	End If
End Sub
Public Sub getLoteamento As Loteamento
	If Loteamento_.IsInitialized Then
		Return Loteamento_
	Else
		Dim da As DBDadosDataAccess
		da.initialize
		Loteamento_ = da.Loteamentos_Where("Id=?", Array(LoteamentoId))
		da.Dispose
		Return Loteamento_
	End If
End Sub
Public Sub getVendas As List
	If Vendas_.IsInitialized Then
		Return Vendas_
	Else
		Dim da As DBDadosDataAccess
		da.initialize
		Vendas_ = da.Vendas_Where2("LoteId=?", Array(Id))
		da.Dispose
		Return Vendas_
	End If
End Sub

#End Region
