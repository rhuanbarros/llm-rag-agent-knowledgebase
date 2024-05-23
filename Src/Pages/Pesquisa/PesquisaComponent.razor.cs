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
                Index_name = "index2",
                Query = inputPesquisa,
                // Alpha = 0.5,
                // Limit = 10
            };

            searchResults = await FrontendClient.Search_semantic_search_semantic__postAsync(queryParams);
        }
    }

    string GetTruncatedContent(string content)
    {
        var length = 600;

        if (content.Length > length)
            return content.Substring(0, length) + "...";
        else
            return content;
    }
}