import logo from './logo.svg';
import './App.css';
import GetCPULoadLastHourView from "./components/CPULastHour";
import CPUCharts from "./components/CPUCharts";
import GetCPULoadLastHourPerMinuteView from "./components/CPULastHourPerMinute";
import LineChart from "./components/Line";

function App() {
  return (
    <div className="App">
      <CPUCharts />
    </div>
  );
}

export default App;
