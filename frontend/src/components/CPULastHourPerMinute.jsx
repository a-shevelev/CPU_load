import React, { useState, useEffect } from "react";
import axios from "axios";
import { Line } from "react-chartjs-2";

const GetCPULoadLastHourPerMinuteView = () => {
  const [cpuLoads, setCpuLoads] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8081/api/cpu_load_per_minute"
        );
        setCpuLoads(response.data.cpu_load);
      } catch (error) {
        console.error("Error fetching average CPU loads per minute:", error);
      }
    };

    fetchData();
  }, []);

  // Преобразование данных для графика
  const chartData = {
    labels: Object.keys(cpuLoads),
    datasets: [
      {
        label: "Average CPU Load per Minute",
        fill: false,
        lineTension: 0.1,
        backgroundColor: "rgba(75,192,192,0.4)",
        borderColor: "rgba(75,192,192,1)",
        borderCapStyle: "butt",
        borderDash: [],
        borderDashOffset: 0.0,
        borderJoinStyle: "miter",
        pointBorderColor: "rgba(75,192,192,1)",
        pointBackgroundColor: "#fff",
        pointBorderWidth: 1,
        pointHoverRadius: 5,
        pointHoverBackgroundColor: "rgba(75,192,192,1)",
        pointHoverBorderColor: "rgba(220,220,220,1)",
        pointHoverBorderWidth: 2,
        pointRadius: 1,
        pointHitRadius: 10,
        data: Object.values(cpuLoads),
      },
    ],
  };

  return (
    <div>
      <h2>Average CPU Load per Minute</h2>
      <Line data={chartData} />
    </div>
  );
};

export default GetCPULoadLastHourPerMinuteView;
