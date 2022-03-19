import styles from "./StreetLampMarker.module.css";

class StreetLampMarker {
  constructor({ type, properties, geometry }, callback) {
    console.log(callback);
    const { iconSize, name } = properties;

    const el = document.createElement("div");
    const width = iconSize[0];
    const height = iconSize[1];
    el.className = styles.marker;
    el.style.backgroundImage = `url(/street-light.png)`;
    el.style.width = `${width}px`;
    el.style.height = `${height}px`;
    el.style.backgroundSize = "100%";

    el.addEventListener("click", () => {
      callback(name);
      console.log("Clicked");
    });
    this.el = el;
  }
}

export default StreetLampMarker;
