B4J=true
Group=Models
ModulesStructureVersion=1
Type=Class
Version=6.3
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

		Public TesteLote As Object '[]

	'</Columns>
	'<Relationships>
		Private Parcelas_ As List '[Lotes.Id <1N> Parcelas.LoteId]

		Private Loteamento_ As Loteamento '[Lotes.LoteamentoId <N1> Loteamentos.Id]

		Private Vendas_ As List '[Lotes.Id <1N> Vendas.LoteId]

	'</Relationships>
End Sub
Public Sub Initialize

End Sub
#Region Relationships
'Lotes.Id <1N> Parcelas.LoteId
Public Sub getParcelas As List
	If Parcelas_.IsInitialized then
		Return Parcelas_
	Else
		Dim da As DBDadosDataAccess
		da.Initialize
		Parcelas_ = da.Parcelas_Where2("LoteId=?", Array(Id))
		da.Dispose
		Return Parcelas_
	End If
End Sub
'Lotes.LoteamentoId <N1> Loteamentos.Id
Public Sub getLoteamento As Loteamento
	If Loteamento_.IsInitialized then
		Return Loteamento_
	Else
		Dim da As DBDadosDataAccess
		da.Initialize
		Loteamento_ = da.Loteamentos_Where("Id=?", Array(LoteamentoId))
		da.Dispose
		Return Loteamento_
	End If
End Sub
'Lotes.Id <1N> Vendas.LoteId
Public Sub getVendas As List
	If Vendas_.IsInitialized then
		Return Vendas_
	Else
		Dim da As DBDadosDataAccess
		da.Initialize
		Vendas_ = da.Vendas_Where2("LoteId=?", Array(Id))
		da.Dispose
		Return Vendas_
	End If
End Sub
#End Region

#Region Subs
	'Write here the subs you want to save
#End Region


#Region Subs
	'Write here the subs you want to save
#End Region

