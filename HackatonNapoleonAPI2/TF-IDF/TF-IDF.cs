namespace VectorizedSearch.TF_IDF;

using System.Text;
using HackatonNapoleonAPI.LinearMath;

public class TfIdf
{
    private int _docsCount;

    private string[] _terms;

    private string[] _docs;
    
    private readonly List<string> _sourceStrings;

    public Matrix TF { get; private set; }
    
    public Vector Vector { get; private set; }
    
    public Matrix TF_IDF { get; private set; }
    
    private Dictionary<string, List<string>> Index { get; set; }

    public TfIdf(List<string> sourceStrings)
    {
        _sourceStrings = sourceStrings;
        
        Init();
        CalcTF();
        CalcIDF();
        CalcTF_IDF();
    }

    public void SetCustomTerms(string[] newTerms)
    {
        _terms = newTerms;
    }

    public void CalcTF_IDF()
    {
        foreach (var doc in _docs)
        {
            foreach (var term in _terms)
            {
                TF_IDF[term, doc] = TF[term, doc] * Vector[term];
            }
        }
    }

    public void CalcIDF()
    {
        foreach (var term in _terms)
        {
            decimal freq = Index[term].Distinct().Count();
            var val = freq == 0 ? 0 : _docsCount / freq;
            Vector[term] = (decimal)Math.Log((double)val);
        }
    }

    public void CalcTF()
    {
        foreach (var doc in _sourceStrings)
        {
            var words = doc.Split(' ');
                
            foreach (var term in _terms)
            {
                decimal entries = words.Count(t => t.Equals(term));
                TF[term, doc] = entries / words.Length;
            }
        }
    }
    
    public Vector QueryIntoVector(string q)
    {
        var v = new Vector(_terms);
        var qs = q.Split(' ');
        var intersect = _terms.Intersect(qs);

        if (!intersect.Any())
        {
            return v;
        }
        
        var gs = intersect.GroupBy(t => t);

        foreach (var g in gs)
        {
            var tf = (decimal)g.ToArray().Length / qs.Length;
            decimal freq = Index[g.Key].Distinct().Count();
            var val = freq == 0 ? 0 : _docsCount / freq;
            var idf = (decimal)Math.Log((double)val);;

            v[g.Key] = tf * idf;
        }

        return v;
    }

    public List<string> Search(string q)
    {
        var v = QueryIntoVector(q);
        var r = new List<(string, double)>();
        
        foreach (var doc in _docs)
        {
            var d = TF_IDF[doc];
            
            var dis = Accord.Math.Distance.Cosine(d.GetValues.Select(v => (double)v).ToArray(),
                v.GetValues.Select(v => (double)v).ToArray());

            if (dis != 1.0)
            {
                r.Add((doc, dis));
            }
        }

        return r.Select(x => x.Item1).ToList();
    }
    
    private void Init()
    {
        Index = new Dictionary<string, List<string>>();

        
        _docs = _sourceStrings.ToArray();
        _docsCount = _docs.Length;
        
        try
        {
            foreach (var f in _sourceStrings)
            {
                foreach (var token in f.Split(' '))
                {
                    if (Index.ContainsKey(token))
                    {
                        Index[token].Add(f);
                    }
                    else
                    {
                        Index.Add(token, new List<string> { f });
                    }
                }
            }
        }
        catch (Exception e)
        {
            Console.WriteLine(e);
        }

        _terms = Index.Keys.ToArray();

        TF = new Matrix(_terms, _docs);
        Vector = new Vector(_terms);
        TF_IDF = new Matrix(_terms, _docs);
    }

    private void ReadTfIdf(string dirWithTfIdf)
    {
        throw new NotImplementedException();
    }
}