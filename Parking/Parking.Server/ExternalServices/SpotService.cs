using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Threading.Tasks;
using Newtonsoft.Json;
using Parking.Server.Models;

public class SpotService
{
    private readonly HttpClient _httpClient;

    public SpotService(HttpClient httpClient)
    {
        _httpClient = httpClient ?? throw new ArgumentNullException(nameof(httpClient));
    }

    public async Task<IEnumerable<Space>> GetSpots()
    {
        try
        {
            var response = await _httpClient
                .GetAsync("http://localhost:5000/api/parking/space");

            if (response.IsSuccessStatusCode)
            {
                var responseBody = await response.Content.ReadAsStringAsync();
                return JsonConvert.DeserializeObject<IEnumerable<Space>>(responseBody);
            }
            else
            {
                throw new HttpRequestException($"Erro ao chamar a API externa: {response.StatusCode}");
            }
        }
        catch (Exception ex)
        {
            throw new Exception("Erro ao chamar a API externa", ex);
        }
    }
}
