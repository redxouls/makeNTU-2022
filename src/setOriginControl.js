class SetOriginControl {
  constructor(options) {
    this._options = Object.assign({}, this._options, options);
  }
  onAdd(map, cs) {
    this.map = map;
    this.container = document.createElement("div");
    this.container.className = `${this._options.className}`;

    const button = this._createButton("monitor_button");
    this.container.appendChild(button);
    return this.container;
  }

  onRemove() {
    this.container.parentNode.removeChild(this.container);
    this.map = undefined;
  }

  _createButton(className) {
    const el = window.document.createElement("button");
    el.className = className;
    el.textContent = "Use my location";
    el.addEventListener(
      "click",
      (e) => {
        this._options.locateCallback();
      },
      false
    );
    return el;
  }
}

export default SetOriginControl;
