export default class setOriginControl {
  constructor(options) {
    this._options = Object.assign({}, this._options, options);
    console.log("setOriginToggle");
  }

  onAdd(map) {
    this._map = map;

    this._btn = document.createElement("button");
    this._btn.className = "mapboxgl-ctrl-icon mapboxgl-ctrl-current-location";
    this._btn.type = "button";
    this._btn["aria-label"] = "Toggle To Set Origin";

    this._btn.onclick = () => {
      this._options.updateCallback();
    };

    this._container = document.createElement("div");
    this._container.className = "mapboxgl-ctrl mapboxgl-ctrl-group";
    this._container.appendChild(this._btn);

    return this._container;
  }

  onRemove() {
    this._container.parentNode.removeChild(this._container);
    this._map = undefined;
  }
}
