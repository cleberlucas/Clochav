using Microsoft.AspNetCore.Mvc;
using Parking.Server.Models;

namespace Parking.Server.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class ParkingController : ControllerBase
    {
        private readonly ILogger<ParkingController> _logger;
        private readonly SpotService _spotService;

        public ParkingController(ILogger<ParkingController> logger, SpotService spotService)
        {
            _logger = logger;
            _spotService = spotService;
        }

        [HttpGet("", Name = "Space")]
        public async Task<IEnumerable<Space>> GetSpot()
        {
            var result = new List<Space>();

            result =  (await _spotService.GetSpots()).ToList();

            return result;
        }

        [HttpGet("Example", Name = "SpotExample")]
        public IEnumerable<Space> GetSpotExample()
        {
            var result = new List<Space>();
            var alphabet = "abcdefgh";

            foreach (var letter in alphabet)
            {
                result.Add(
                    new Space()
                    {
                        Floor = 1,
                        Spot = letter,
                        Used = Random.Shared.Next(0, 10) % 2 == 0
                    }
                );
            }

            return result;
        }
    }
}
