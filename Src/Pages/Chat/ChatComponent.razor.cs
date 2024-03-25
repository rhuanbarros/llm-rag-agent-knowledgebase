using Microsoft.AspNetCore.Components;

namespace Procurador.Web.Src.Pages.Chat;

public partial class ChatComponent : ComponentBase
{
    protected string inputPesquisa { get; set; } = "";

    // protected ICollection<SearchResult> mensagens;

    public async Task OnClickPesquisa()
    {
        if(!string.IsNullOrEmpty(inputPesquisa))
        {
        }
    }

}