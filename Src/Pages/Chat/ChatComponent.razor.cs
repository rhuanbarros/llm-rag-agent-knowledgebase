using Microsoft.AspNetCore.Components;
using Procurador.Web.Src.Services.Base;

namespace Procurador.Web.Src.Pages.Chat;

public partial class ChatComponent : ComponentBase
{
    [Inject] IFrontendClient FrontendClient { get; set; }

    protected string inputChat { get; set; } = "";

    protected List<MessageModel> ChatHistory = new();

    public async Task OnClickPesquisa()
    {
        if(!string.IsNullOrEmpty(inputChat))
        {
            MessageModel messageModel = new() 
            {
                Type = "Human",
                Content = inputChat
            };
            ChatHistory.Add(messageModel);
            inputChat = "";

            MessageModel aiMessage = await FrontendClient.Chat_chat__postAsync(ChatHistory);
            ChatHistory.Add(aiMessage);
            
            await InvokeAsync(StateHasChanged);
        }
    }

}