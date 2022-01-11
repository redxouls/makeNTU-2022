import logo from "./location-arrow.svg";

const LocationMarker = (iconSize = [30, 30]) => {
  // Create a DOM element for each marker.
  const [width, height] = iconSize;

  // create div tag and set style
  const el = document.createElement("div");
  el.className = "marker";
  el.style.width = `${width}px`;
  el.style.height = `${height}px`;
  el.style.backgroundSize = "100%";

  // create img tag and set style
  const img = document.createElement("img");
  img.src = logo;
  img.backgroundColor = "#03030a";
  img.style.transform = "rotateZ(-45deg)";

  el.appendChild(img);
  console.log(el.style);

  return el;
};

export default LocationMarker;
