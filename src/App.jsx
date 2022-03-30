import React, { useEffect, useRef, useState } from "react";
import {
  CustomProvider,
  Drawer,
  Placeholder,
  Notification,
  // Slider,
  Divider,
  toaster,
} from "rsuite";

import LightController from "./components/LightController";

import LightModeIcon from "@mui/icons-material/LightMode";

import "rsuite/dist/rsuite.min.css";

import "./App.css";

import Chart from "./components/Chart";

import Map from "./components/Map.js";
import VideoJS from "./Video"; // point to where the functional component is stored

const { Paragraph } = Placeholder;

class State {
  constructor() {
    this.index = 0;
  }
  setIndex(index) {
    this.index = index;
  }
}
const state = new State();

const App = () => {
  const mapRef = useRef(null);
  const playerRef = useRef(null);

  const [mapApp, setMapApp] = useState(null);
  const [open, setOpen] = useState(false);
  const [header, setHeader] = useState("");

  const handleShowDetail = (index, name) => {
    setOpen(true);
    setHeader(name);
    state.setIndex(index);
  };

  const handlers = {
    handleShowDetail,
  };

  const videoJsOptions = {
    // lookup the options in the docs for more options
    autoplay: true,
    controls: true,
    responsive: true,
    fluid: true,
    sources: [
      {
        src: "/video/playlist.m3u8",
        type: "application/x-mpegURL",
      },
    ],
  };

  const handlePlayerReady = (player) => {
    playerRef.current = player;

    // you can handle player events here
    player.on("waiting", () => {
      console.log("player is waiting");
    });

    player.on("dispose", () => {
      console.log("player will dispose");
    });
  };

  useEffect(() => {
    const mapApp = new Map(mapRef.current, handlers);
    setMapApp(mapApp);
  }, []);

  return (
    <CustomProvider theme="dark">
      <React.Fragment>
        <div ref={mapRef} className="mapWrapper"></div>
        <div>
          <Drawer backdrop={true} open={open} onClose={() => setOpen(false)}>
            <Drawer.Header>
              <Drawer.Title>
                <div style={{ textAlign: "center" }}>
                  <h2>{header}</h2>
                </div>
              </Drawer.Title>
            </Drawer.Header>
            <Drawer.Body>
              <h5>I'm a streetlight from National Taiwan University.</h5>
              <h5>Several Sensors are currently online.</h5>
              <h5>You can adjust my brightness as well.</h5>
              <Divider />
              <div style={{ textAlign: "center" }}>
                <LightModeIcon />
                <h3>Brightness</h3>
              </div>
              <br />
              <LightController state={state} />
              <Divider />
              <div style={{ textAlign: "center" }}>
                <h3>Sensor Data</h3>
              </div>
              <br />
              <Chart state={state} />
              <Divider />
              <div style={{ textAlign: "center" }}>
                <h3>Surveillance Camera</h3>
                <br />
              </div>
              <VideoJS options={videoJsOptions} onReady={handlePlayerReady} />
            </Drawer.Body>
          </Drawer>
        </div>
      </React.Fragment>
    </CustomProvider>
  );
};

export default App;
