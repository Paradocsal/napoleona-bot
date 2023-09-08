namespace HackatonNapoleonAPI.LinearMath;

using System.Text;

public class Vector
{
    private readonly decimal[] _values;
    private readonly string[] _terms;

    public decimal[] GetValues => _values;

    public Vector(string[] terms)
    {
        _values = new decimal[terms.Length];
        _terms = terms;
    }

    public decimal this[string term]
    {
        get => _values[Array.IndexOf(_terms, term)];
        set => _values[Array.IndexOf(_terms, term)] = value;
    }

    public void SaveAs(string @as)
    {
        var p = Path.Join(Directory.GetCurrentDirectory(), @as);

        using (var sr = new StreamWriter(File.Create(p), Encoding.UTF8))
        {
            sr.WriteLine(string.Join(";", _terms));
            sr.WriteLine(String.Join(";", _values));
        }
    }
}