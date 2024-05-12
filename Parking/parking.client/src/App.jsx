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
            <thead>
                <tr>
                    <th>Floor</th>
                    <th>Space</th>
                    <th>Reserve</th>
                </tr>
            </thead>
            <tbody>
                {spaces.map(space =>
                    <tr key={space.floor}>
                        <td>{space.floor}</td>
                        <td>{space.space}</td>
                        <td className={space.used ? 'space-occupied' : 'space-empty'}>{space.used ? 'OCCUPIED' : 'VACANT'}</td>
                    </tr>
                )}
            </tbody>
        </table>;

    return (
        <div className="menu">
            <h1 id="tabelLabel">Parking Vacancies Monitor</h1>
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
            const response = await fetch('http://127.0.0.1:5000/api/parking/space');
            const data = await response.json();
            setParkings(data);

        } catch (ex) {
            console.error('Error Fetching Parking Data:', ex);
        }
    }

    function startParkingDataPolling() {
        const intervalId = setInterval(() => {
            populateParkingData();
        }, 1000);

        return () => clearInterval(intervalId);
    }
}

export default App;
