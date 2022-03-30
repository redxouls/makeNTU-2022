import React from "react";
import Slider from "@mui/material/Slider";
import { _ } from "lodash";

import { StreetAPI } from "../api";

import "./LightController.css";

const LightController = (props) => {
  const marks = [
    {
      value: 0,
      label: "0%",
    },
    {
      value: 25,
      label: "25%",
    },
    {
      value: 50,
      label: "50%",
    },
    {
      value: 75,
      label: "75%",
    },
    {
      value: 100,
      label: "100%",
    },
  ];

  function valuetext(value) {
    return <h5>{`${value}%`}</h5>;
  }

  return (
    <Slider
      aria-label="Always visible"
      defaultValue={80}
      getAriaValueText={valuetext}
      step={5}
      marks={marks}
      valueLabelDisplay="on"
      style={{ color: "#91a7eb" }}
      onChange={_.throttle((e) => {
        const payload = {
          to: props.state.index,
          brightness: e.target.value,
        };
        StreetAPI.postBrightness(payload).then((response) => {
          console.log(response);
        });
      }, 100)}
    />
  );
};

export default LightController;
