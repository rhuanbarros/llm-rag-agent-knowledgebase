using Microsoft.AspNetCore.Components.Web;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
using MudBlazor.Services;
using Procurador.Web;
using Procurador.Web.Src.Services.Base;

var builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.RootComponents.Add<App>("#app");
builder.RootComponents.Add<HeadOutlet>("head::after");

// builder.Services.AddScoped(sp => new HttpClient { BaseAddress = new Uri(builder.HostEnvironment.BaseAddress) });
builder.Services.AddHttpClient<IData_managementClient, Data_managementClient>(cl => cl.BaseAddress = new Uri(builder.Configuration.GetValue<string>("API_URL")));
builder.Services.AddHttpClient<IFrontendClient, FrontendClient>(cl => cl.BaseAddress = new Uri(builder.Configuration.GetValue<string>("API_URL")));

builder.Services.AddMudServices();

await builder.Build().RunAsync();
