import React, { useState, useEffect } from "react";
import axios from "axios";
import { Line } from "react-chartjs-2";

const GetCPULoadLastHourView = () => {
  const [cpuLoads, setCpuLoads] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8081/api/cpu_load_last_hour"
        );
        setCpuLoads(response.data.cpu_load);
        setIsLoading(false);
      } catch (error) {
        console.error("Ошибка при получении данных о загрузке CPU:", error);
        setError(error.message);
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  if (isLoading) return <div>Загрузка...</div>;
  if (error) return <div>Ошибка: {error}</div>;

  const chartData = {
    labels: cpuLoads.map((load) =>
      new Date(load.timestamp).toLocaleTimeString()
    ),
    datasets: [
      {
        label: "Загрузка CPU",
        data: cpuLoads.map((load) => load.load),
        fill: false,
        borderColor: "rgba(75,192,192,1)",
        backgroundColor: "rgba(75,192,192,0.4)",
        pointBorderColor: "rgba(75,192,192,1)",
        pointBackgroundColor: "#fff",
        pointBorderWidth: 1,
        pointHoverRadius: 5,
        pointHoverBackgroundColor: "rgba(75,192,192,1)",
        pointHoverBorderColor: "rgba(220,220,220,1)",
        pointHoverBorderWidth: 2,
        pointRadius: 1,
        pointHitRadius: 10,
      },
    ],
  };

  const chartOptions = {
    scales: {
      x: {
        title: {
          display: true,
          text: "Время",
        },
      },
      y: {
        title: {
          display: true,
          text: "Загрузка CPU (%)",
        },
        beginAtZero: true,
      },
    },
  };

  return (
    <div>
      <h2>Загрузка CPU за последний час</h2>
      <Line data={chartData} options={chartOptions} />
    </div>
  );
};

export default GetCPULoadLastHourView;
