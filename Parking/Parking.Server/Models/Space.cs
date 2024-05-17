namespace Parking.Server.Models
{
    public class Space
    {
        public int Floor { get; set; }


        private char spot { get ; set; }
        public char Spot { 
            get => spot.ToString().ToUpper().ToCharArray()[0];
            set => spot = value; 
        }

        public bool Used { get; set; }

    }
}
