namespace HackatonNapoleonAPI.LinearMath;

using System.Text;

public class Matrix
{
    private readonly decimal[][] _values;
    private readonly string[] _terms;
    private readonly string[] _docs;

    public string[] GetTerms => _terms;
    public string[] GetDocs => _docs;

    public Matrix(string[] terms, string[] docs)
    {
        _values = new decimal[terms.Length][];

        foreach (var i in Enumerable.Range(0, terms.Length))
        {
            _values[i] = new decimal[docs.Length];
        }
        
        _terms = terms;
        _docs = docs;
    }
    
    public Vector this[string doc]
    {
        get
        {
            var v = new Vector(_terms);
            var i = Array.IndexOf(_docs, doc);

            foreach (var t in _terms)
            {
                v[t] = _values[Array.IndexOf(_terms, t)][i];
            }

            return v;
        }
    }

    public decimal this[string term, string doc]
    {
        get => _values[Array.IndexOf(_terms, term)][Array.IndexOf(_docs, doc)];
        set => _values[Array.IndexOf(_terms, term)][Array.IndexOf(_docs, doc)] = value;
    }

    public void SaveAs(string @as)
    {
        var p = Path.Join(Directory.GetCurrentDirectory(), @as);

        using (var sr = new StreamWriter(File.Create(p), Encoding.UTF8))
        {
            sr.WriteLine(";" + string.Join(";", _docs.Select(Path.GetFileName)));
            
            for (int i = 0; i < _terms.Length; i++)
            {
                sr.Write(_terms[i] + ";");
            
                for (int j = 0; j < _docs.Length; j++)
                {
                    sr.Write(_values[i][j] + ";");
                }
            
                sr.WriteLine();
            }
        }
    }
}