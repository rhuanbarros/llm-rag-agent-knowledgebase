using Microsoft.AspNetCore.Components;

namespace Procurador.Web.Src.Pages.Pesquisa;

public partial class PesquisaComponent : ComponentBase
{
//     [Inject] IClient Client { get; set; }

    public string inputPesquisa { get; set; } = "";
    public bool primeiraPesquisa {get;set;} = true;

    protected override async Task OnParametersSetAsync()
    {
    }

    // ICollection<SearchResult> searchResults;
    public async Task OnClickPesquisa()
    {
        // if(!string.IsNullOrEmpty(inputPesquisa))
        // {
        //     primeiraPesquisa = false;

        //     QueryParams queryParams = new()
        //     {
        //         Collection = "",
        //         Query = inputPesquisa,
        //         // Alpha = 0.5,
        //         // Limit = 10
        //     };

        //     searchResults = await Client.Process_query_process_query__postAsync(queryParams);
        // }
    }

    string GetTruncatedContent(string content)
    {
        if (content.Length > 200)
            return content.Substring(0, 200) + "...";
        else
            return content;
    }
}