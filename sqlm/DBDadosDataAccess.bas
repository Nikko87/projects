B4J=true
Group=Controllers
ModulesStructureVersion=1
Type=Class
Version=6.3
@EndOfDesignText@
Sub Class_Globals
	Private fx as JFX
	Private SQL1 As SQL
End Sub

Public Sub initialize
	SQL1.InitializeSQLite(File.DirApp, "DBDados.db", True)
End Sub
Public Sub Dispose
	SQL1.Close
End Sub

Public Sub getSQL As SQL
	Return SQL1
End Sub

#Region Subs
	'Write here the subs you want to save
#End Region


#Region Table <Lotes>

Public Sub Lotes_CreateTable()
	Dim mData As Map
	mData.Initialize
	mData.Put("Id", "Integer PRIMARY KEY ASC AUTOINCREMENT")
	mData.Put("LoteamentoId", "Integer REFERENCES Loteamentos (Id)")
	mData.Put("Quadra", "String NOT NULL")
	mData.Put("Lote", "String NOT NULL")
	mData.Put("Area", "Double")
	mData.Put("Preco", "Double")
	mData.Put("Situacao", "Integer NOT NULL")
	mData.Put("TesteLote", "Blob")
	DBUtils.CreateTable(SQL1, "Lotes", mData, "")
End Sub

Public Sub Lotes_Insert(t As Lote)
	Dim m As Map
	m.Initialize
	m.Put("LoteamentoId", t.LoteamentoId)
	m.Put("Quadra", t.Quadra)
	m.Put("Lote", t.Lote)
	m.Put("Area", t.Area)
	m.Put("Preco", t.Preco)
	m.Put("Situacao", t.Situacao)
	m.Put("TesteLote", t.TesteLote)
	DBUtils.InsertMaps(SQL1, "Lotes", Array As Object(m))
End Sub

Public Sub Lotes_Insert2(LoteamentoId As Int, Quadra As String, Lote As String, Area As Double, Preco As Double, Situacao As Int, TesteLote As Object)
	Dim m As Map
	m.Initialize
	m.Put("LoteamentoId", LoteamentoId)
	m.Put("Quadra", Quadra)
	m.Put("Lote", Lote)
	m.Put("Area", Area)
	m.Put("Preco", Preco)
	m.Put("Situacao", Situacao)
	m.Put("TesteLote", TesteLote)
	DBUtils.InsertMaps(SQL1, "Lotes", Array As Object(m))
End Sub

Public Sub Lotes_Delete(t As Lote)
	Dim m As Map = CreateMap("Id": t.Id)
	DBUtils.DeleteRecord(SQL1, "Lotes", m)
End Sub

Public Sub Lotes_Update(t As Lote)
	Dim m As Map
	m.Initialize
	m.Put("LoteamentoId", t.LoteamentoId)
	m.Put("Quadra", t.Quadra)
	m.Put("Lote", t.Lote)
	m.Put("Area", t.Area)
	m.Put("Preco", t.Preco)
	m.Put("Situacao", t.Situacao)
	m.Put("TesteLote", t.TesteLote)
	Dim WhereFields As Map = CreateMap("Id": t.Id)
	DBUtils.UpdateRecord2(SQL1, "Lotes", m, WhereFields)
End Sub

Public Sub Lotes_GetById(Id As Int) As Lote
	Return Lotes_Where("Id=?", Array(Id))
End Sub

Public Sub Lotes_ToList As List
	Dim rs As ResultSet
	Dim lstResult As List
	lstResult.Initialize
	rs = SQL1.ExecQuery("SELECT * FROM Lotes")
	Do While rs.NextRow
		Dim t As Lote
		t.Initialize
		t.Id = rs.GetInt("Id")
		t.LoteamentoId = rs.GetInt("LoteamentoId")
		t.Quadra = rs.GetString("Quadra")
		t.Lote = rs.GetString("Lote")
		t.Area = rs.GetDouble("Area")
		t.Preco = rs.GetDouble("Preco")
		t.Situacao = rs.GetInt("Situacao")
		t.TesteLote = rs.GetObject("TesteLote")
		lstResult.Add(t)
	Loop
	Return lstResult
End Sub

Public Sub Lotes_Where(WhereCondition As String, ArgList As List) As Lote
	Dim rs As ResultSet
	rs = SQL1.ExecQuery2("SELECT * FROM Lotes WHERE " & WhereCondition, ArgList)
	If rs.NextRow = False Then Return Null
	Dim t As Lote
	t.Initialize
	t.Id = rs.GetInt("Id")
	t.LoteamentoId = rs.GetInt("LoteamentoId")
	t.Quadra = rs.GetString("Quadra")
	t.Lote = rs.GetString("Lote")
	t.Area = rs.GetDouble("Area")
	t.Preco = rs.GetDouble("Preco")
	t.Situacao = rs.GetInt("Situacao")
	t.TesteLote = rs.GetObject("TesteLote")
	Return t
End Sub

Public Sub Lotes_Where2(WhereCondition As String, ArgList As List) As List
	Dim rs As ResultSet
	Dim lstResult As List
	lstResult.Initialize
	rs = SQL1.ExecQuery2("SELECT * FROM Lotes WHERE " & WhereCondition, ArgList)
	Do While rs.NextRow
		Dim t As Lote
		t.Initialize
		t.Id = rs.GetInt("Id")
		t.LoteamentoId = rs.GetInt("LoteamentoId")
		t.Quadra = rs.GetString("Quadra")
		t.Lote = rs.GetString("Lote")
		t.Area = rs.GetDouble("Area")
		t.Preco = rs.GetDouble("Preco")
		t.Situacao = rs.GetInt("Situacao")
		t.TesteLote = rs.GetObject("TesteLote")
		lstResult.Add(t)
	Loop
	Return lstResult
End Sub

Public Sub Lotes_RowCount() As Int
	Return SQL1.ExecQuerySingleResult("SELECT Count(*) FROM Lotes")
End Sub

#End Region
#Region Table <Loteamentos>

Public Sub Loteamentos_CreateTable()
	Dim mData As Map
	mData.Initialize
	mData.Put("Id", "Integer PRIMARY KEY ASC AUTOINCREMENT")
	mData.Put("Nome", "String NOT NULL")
	mData.Put("Cidade", "String NOT NULL")
	mData.Put("Numlotes", "Integer NOT NULL")
	mData.Put("Teste1", "String")
	DBUtils.CreateTable(SQL1, "Loteamentos", mData, "")
End Sub

Public Sub Loteamentos_Insert(t As Loteamento)
	Dim m As Map
	m.Initialize
	m.Put("Nome", t.Nome)
	m.Put("Cidade", t.Cidade)
	m.Put("Numlotes", t.Numlotes)
	m.Put("Teste1", t.Teste1)
	DBUtils.InsertMaps(SQL1, "Loteamentos", Array As Object(m))
End Sub

Public Sub Loteamentos_Insert2(Nome As String, Cidade As String, Numlotes As Int, Teste1 As String)
	Dim m As Map
	m.Initialize
	m.Put("Nome", Nome)
	m.Put("Cidade", Cidade)
	m.Put("Numlotes", Numlotes)
	m.Put("Teste1", Teste1)
	DBUtils.InsertMaps(SQL1, "Loteamentos", Array As Object(m))
End Sub

Public Sub Loteamentos_Delete(t As Loteamento)
	Dim m As Map = CreateMap("Id": t.Id)
	DBUtils.DeleteRecord(SQL1, "Loteamentos", m)
End Sub

Public Sub Loteamentos_Update(t As Loteamento)
	Dim m As Map
	m.Initialize
	m.Put("Nome", t.Nome)
	m.Put("Cidade", t.Cidade)
	m.Put("Numlotes", t.Numlotes)
	m.Put("Teste1", t.Teste1)
	Dim WhereFields As Map = CreateMap("Id": t.Id)
	DBUtils.UpdateRecord2(SQL1, "Loteamentos", m, WhereFields)
End Sub

Public Sub Loteamentos_GetById(Id As Int) As Loteamento
	Return Loteamentos_Where("Id=?", Array(Id))
End Sub

Public Sub Loteamentos_ToList As List
	Dim rs As ResultSet
	Dim lstResult As List
	lstResult.Initialize
	rs = SQL1.ExecQuery("SELECT * FROM Loteamentos")
	Do While rs.NextRow
		Dim t As Loteamento
		t.Initialize
		t.Id = rs.GetInt("Id")
		t.Nome = rs.GetString("Nome")
		t.Cidade = rs.GetString("Cidade")
		t.Numlotes = rs.GetInt("Numlotes")
		t.Teste1 = rs.GetString("Teste1")
		lstResult.Add(t)
	Loop
	Return lstResult
End Sub

Public Sub Loteamentos_Where(WhereCondition As String, ArgList As List) As Loteamento
	Dim rs As ResultSet
	rs = SQL1.ExecQuery2("SELECT * FROM Loteamentos WHERE " & WhereCondition, ArgList)
	If rs.NextRow = False Then Return Null
	Dim t As Loteamento
	t.Initialize
	t.Id = rs.GetInt("Id")
	t.Nome = rs.GetString("Nome")
	t.Cidade = rs.GetString("Cidade")
	t.Numlotes = rs.GetInt("Numlotes")
	t.Teste1 = rs.GetString("Teste1")
	Return t
End Sub

Public Sub Loteamentos_Where2(WhereCondition As String, ArgList As List) As List
	Dim rs As ResultSet
	Dim lstResult As List
	lstResult.Initialize
	rs = SQL1.ExecQuery2("SELECT * FROM Loteamentos WHERE " & WhereCondition, ArgList)
	Do While rs.NextRow
		Dim t As Loteamento
		t.Initialize
		t.Id = rs.GetInt("Id")
		t.Nome = rs.GetString("Nome")
		t.Cidade = rs.GetString("Cidade")
		t.Numlotes = rs.GetInt("Numlotes")
		t.Teste1 = rs.GetString("Teste1")
		lstResult.Add(t)
	Loop
	Return lstResult
End Sub

Public Sub Loteamentos_RowCount() As Int
	Return SQL1.ExecQuerySingleResult("SELECT Count(*) FROM Loteamentos")
End Sub

#End Region