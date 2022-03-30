import React, { useState, useEffect } from "react";
import {
  AreaChart,
  Area,
  Tooltip,
  CartesianGrid,
  XAxis,
  YAxis,
} from "recharts";
import colormap from "colormap";

import "./Chart.css";

import { StreetAPI } from "../api";

const Chart = ({ state }) => {
  const [rawData, setRawData] = useState([]);
  let colors = colormap({
    colormap: "hsv",
    nshades: 20,
    format: "hex",
    alpha: 0.8,
  });
  console.log(colors);

  useEffect(() => {
    setInterval(() => {
      const { index } = state;
      StreetAPI.getSensorByIndex(index).then((response) => {
        setRawData(response.data);
      });
    }, 2000);
  }, []);

  return Object.entries(rawData).map(([type, data], i) => {
    return (
      <React.Fragment key={type}>
        <div style={{ textAlign: "center" }}>
          <h4>{type}</h4>
        </div>
        <AreaChart
          width={450}
          height={250}
          data={data}
          margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
        >
          <defs>
            <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8} />
              <stop offset="95%" stopColor="#8884d8" stopOpacity={0} />
            </linearGradient>
          </defs>

          <XAxis dataKey={"time"} type={"category"} />
          <YAxis />
          <CartesianGrid strokeDasharray="3 3" />
          <Tooltip />
          <Area
            type="monotone"
            dataKey={type}
            stroke={colors[i * 2 + 14]}
            fillOpacity={0.7}
            fill={colors[i * 2 + 14]}
          />
        </AreaChart>
      </React.Fragment>
    );
  });
};

export default Chart;
