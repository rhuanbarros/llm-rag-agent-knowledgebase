using Microsoft.AspNetCore.Components;
using Procurador.Web.Src.Services.Base;

namespace Procurador.Web.Src.Pages.Pesquisa;

public partial class PesquisaComponent : ComponentBase
{
    [Inject] IFrontendClient FrontendClient { get; set; }

    public string inputPesquisa { get; set; } = "";
    public bool primeiraPesquisa {get;set;} = true;

    protected override async Task OnParametersSetAsync()
    {
    }

    ICollection<DocModel> searchResults;
    public async Task OnClickPesquisa()
    {
        if(!string.IsNullOrEmpty(inputPesquisa))
        {
            primeiraPesquisa = false;

            QueryParamsModel queryParams = new()
            {
                Collection = "qdrant_teste1",
                Query = inputPesquisa,
                // Alpha = 0.5,
                // Limit = 10
            };

            searchResults = await FrontendClient.Process_query_process_query__postAsync(queryParams);
        }
    }

    string GetTruncatedContent(string content)
    {
        if (content.Length > 200)
            return content.Substring(0, 200) + "...";
        else
            return content;
    }
}