import React, { useEffect, useRef, useState } from "react";
import "./App.css";

import Map from "./Map.js";

const App = () => {
  const mapRef = useRef(null);
  const [mapApp, setMapApp] = useState(null);

  useEffect(() => {
    const mapApp = new Map(mapRef.current);
    setMapApp(mapApp);
  }, []);

  return <div ref={mapRef} className="mapWrapper"></div>;
};

export default App;
