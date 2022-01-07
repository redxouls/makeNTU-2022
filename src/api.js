import axios from "axios";

const errorHandling = (error) => {
  // if (error.response.status === 403) window.location.replace("/");
  console.log(error);
};

export const PositionAPI = {
  getCurentPosition: () =>
    axios.get(`/api/current/location`).catch((error) => errorHandling(error)),
  getCurentBearing: () =>
    axios.get(`/api/current/bearing`).catch((error) => errorHandling(error)),
  // postNavigation: (data) =>
  //   axios.post(`/api/navigation`, data).catch((error) => errorHandling(error)),
};
