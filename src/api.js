import axios from "axios";

const errorHandling = (error) => {
  // if (error.response.status === 403) window.location.replace("/");
  console.log(error);
};

export const StreetAPI = {
  getAllStreetlights: () =>
    axios.get(`/api/allStreetlights`).catch((error) => errorHandling(error)),
  getAllSensors: () =>
    axios.get(`/api/allSensors`).catch((error) => errorHandling(error)),
  getSensorByIndex: (index) =>
    axios.get(`/api/sensor/${index}`).catch((error) => errorHandling(error)),
  getFallAlarm: () =>
    axios.get(`/api/fall_alarm`).catch((error) => errorHandling(error)),
  postFall: (data) =>
    axios
      .post(`/api/fall`, JSON.stringify(data), {
        headers: {
          "Content-Type": "application/json",
        },
      })
      .catch((error) => errorHandling(error)),
  postObjectPass: (data) =>
    axios
      .post(`/api/obj_passed`, JSON.stringify(data), {
        headers: {
          "Content-Type": "application/json",
        },
      })
      .catch((error) => errorHandling(error)),
  postBrightness: (data) =>
    axios
      .post(`/api/brightness`, JSON.stringify(data), {
        headers: {
          "Content-Type": "application/json",
        },
      })
      .catch((error) => errorHandling(error)),
};
