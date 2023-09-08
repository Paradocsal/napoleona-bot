namespace HackatonNapoleonAPI.Controllers;

using Microsoft.AspNetCore.Mvc;
using VectorizedSearch.TF_IDF;

[ApiController]
[Route("[controller]")]
public class TfIdfSearchController : ControllerBase
{
    private readonly ILogger<TfIdfSearchController> _logger;

    public TfIdfSearchController(
        ILogger<TfIdfSearchController> logger)
    {
        _logger = logger;
    }

    [HttpPost(Name = "Search")]
    public IEnumerable<string> Search(string query, List<string> userNamesList)
    {
        _logger.Log(LogLevel.Debug, $"{DateTime.Now} income query {query}");
        
        return new TfIdf(userNamesList).Search(query);
    }
}