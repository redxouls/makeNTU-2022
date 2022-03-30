import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App";
import * as serviceWorker from "./serviceWorker";
import { Notification, toaster } from "rsuite";
import { StreetAPI } from "./api";

const handleAlert = (msg) => {
  toaster.push(
    <Notification type={"warning"} header={"warning"} closable>
      {msg}
    </Notification>,
    { placement: "topCenter" }
  );
};

setInterval(() => {
  StreetAPI.getFallAlarm().then((response) => {
    const { data: fallEvents } = response;
    if (fallEvents.fall) {
      const { timeString, index, probability } = fallEvents;
      handleAlert(
        <div>
          <p>{`TimeStamp: ${timeString}`}</p>
          <p>{`Fall Event Detected: StreetLight #${index}`}</p>
          <p>{`Probability: ${probability}`}</p>
        </div>
      );
    }
  });
}, 1000);

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById("root")
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
