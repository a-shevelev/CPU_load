import React, { useState, useEffect } from "react";
import axios from "axios";
import LineChart from "./LineChart";

const CPUCharts = () => {
  const [cpuLoadLastHour, setCpuLoadLastHour] = useState([]);
  const [cpuLoadPerMinute, setCpuLoadPerMinute] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchCPULoadLastHour = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:8081/api/cpu_load_last_hour"
      );
      setCpuLoadLastHour(response.data.cpu_load);
    } catch (error) {
      console.error("Error fetching CPU load for the last hour:", error);
      setError(error.message);
    }
  };

  const fetchCPULoadPerMinute = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:8081/api/cpu_load_per_minute"
      );
      setCpuLoadPerMinute(response.data.cpu_load);
    } catch (error) {
      console.error("Error fetching average CPU loads per minute:", error);
      setError(error.message);
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      await fetchCPULoadLastHour();
      await fetchCPULoadPerMinute();
      setIsLoading(false);
    };

    fetchData();

    const interval = setInterval(() => {
      fetchData();
    }, 10000); // Fetch data every 10 seconds

    return () => clearInterval(interval);
  }, []);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <LineChart
        data={cpuLoadLastHour}
        title={"Загрузка CPU за последний час"}
      />
      <LineChart
        data={cpuLoadPerMinute}
        title={"Средняя загрузка CPU в минуту"}
      />
    </div>
  );
};

export default CPUCharts;
