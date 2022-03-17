import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";
import MapboxDirections from "@mapbox/mapbox-gl-directions/dist/mapbox-gl-directions";
import "@mapbox/mapbox-gl-directions/dist/mapbox-gl-directions.css";

mapboxgl.accessToken =
  "pk.eyJ1IjoicmVkeG91bHMiLCJhIjoiY2t4N2R1Nm1uMHl4aTJwcXViYno1Ym9sNCJ9.fByzZrach_1gQlboB02hCg";

class Map {
  constructor(ref) {
    this.navigating = false;
    this.container = ref;
    this.map = new mapboxgl.Map({
      container: this.container,
      style: "mapbox://styles/mapbox/streets-v11",
      center: [121.54373533333333, 25.0190466666666684],
      zoom: 16,
    });

    const navigation = new mapboxgl.NavigationControl({ showCompass: false });
    this.map.addControl(navigation);

    // const coordinates = [121.54373533333333, 25.0190466666666684];

    // this.currentMarker = new mapboxgl.Marker()
    //   .setLngLat(coordinates)
    //   .setRotation(0)
    //   .addTo(this.map);
  }
}

export default Map;
