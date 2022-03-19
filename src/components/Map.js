import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";

import MapboxDirections from "@mapbox/mapbox-gl-directions/dist/mapbox-gl-directions";
import "@mapbox/mapbox-gl-directions/dist/mapbox-gl-directions.css";

import StreetLampMarker from "./markers/StreetLampMarker";

import { StreetAPI } from "../api";

mapboxgl.accessToken =
  "pk.eyJ1IjoicmVkeG91bHMiLCJhIjoiY2t4N2R1Nm1uMHl4aTJwcXViYno1Ym9sNCJ9.fByzZrach_1gQlboB02hCg";

class Map {
  constructor(ref) {
    this.navigating = false;
    this.container = ref;
    this.map = new mapboxgl.Map({
      container: this.container,
      style: "mapbox://styles/mapbox/dark-v9",
      center: [121.54591, 25.01876],
      zoom: 18,
      pitch: 60, // pitch in degrees
    });

    const navigation = new mapboxgl.NavigationControl({ showCompass: false });
    this.map.addControl(navigation);

    StreetAPI.getAllStreetlights().then((response) => {
      const { data: geojson } = response;
      console.log(geojson);
      for (const marker of geojson) {
        // Create a DOM element for each marker.
        const { el } = new StreetLampMarker(marker);
        // Add markers to the map.
        new mapboxgl.Marker(el)
          .setLngLat(marker.geometry.coordinates)
          .addTo(this.map);
      }
    });
    // Add markers to the map.
  }
}

export default Map;
