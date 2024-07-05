import React from "react";
import { Line } from "react-chartjs-2";
import "chartjs-plugin-annotation";

const LineChart = ({ data, title }) => {
  const chartData = {
    labels: data.map((load) => new Date(load.timestamp).toLocaleTimeString()),
    datasets: [
      {
        label: "Загрузка CPU",
        data: data.map((load) => load.load),
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
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "900px",
      }}
    >
      <div style={{ width: "1200px", height: "800px" }}>
        <span>{title}</span>
        <Line data={chartData} options={chartOptions} />
      </div>
    </div>
  );
};

export default LineChart;
