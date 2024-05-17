import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
    //const [forecasts, setForecasts] = useState();
    const [spaces, setParkings] = useState();

    useEffect(() => {
/*        populateWeatherData();*/
        startParkingDataPolling();
    }, []);

    const contents = spaces === undefined
        ? <p><em>Loading... Please refresh once the ASP.NET backend has started. See <a href="https://aka.ms/jspsintegrationreact">https://aka.ms/jspsintegrationreact</a> for more details.</em></p>
        : <table className="table table-striped" aria-labelledby="tabelLabel">
               
            <tr>
                <th>FLOOR</th>
                {spaces.map(space => <td>{space.floor}</td>)}
            </tr>
            <tr>
                <th>SPOT</th>
                {spaces.map(space =><td>{space.spot}</td>)}
            </tr>
            <tr>
                <th>RESERVE</th>
                {spaces.map(space =><td className={space.used ? 'space-occupied' : 'space-empty'}>{space.used ? 'OCCUPIED' : 'VACANT'}</td>)}
            </tr>          
        </table>

    return (
        <div className="menu">
            <h1 id="tabelLabel">MONITOR</h1>
            {contents}
        </div>
    );

    //async function populateWeatherData() {
    //    const response = await fetch('WeatherForecast');
    //    const data = await response.json();
    //    setForecasts(data);
    //}

    async function populateParkingData() {
        try {
            //const response = await fetch('https://localhost:7124/Parking/Space/Example');
            const response = await fetch('https://localhost:7124/Parking/Space');
            const data = await response.json();
            setParkings(data);

        } catch (ex) {
            console.error('Error Fetching Parking Data:', ex);
        }
    }

    function startParkingDataPolling() {
        const intervalId = setInterval(() => {
            populateParkingData();
        }, 500);

        return () => clearInterval(intervalId);
    }
}

export default App;
