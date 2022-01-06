import axios from "axios";

const errorHandling = (error) => {
  // if (error.response.status === 403) window.location.replace("/");
  console.log(error);
};

export const PositionAPI = {
  getCurentPosition: () =>
    axios.get(`/api/current`).catch((error) => errorHandling(error)),
};
