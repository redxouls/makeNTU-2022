import axios from "axios";

const errorHandling = (error) => {
  // if (error.response.status === 403) window.location.replace("/");
  console.log(error);
};

export const StreetAPI = {
  getAllStreetlights: () =>
    axios.get(`/api/allStreetlights`).catch((error) => errorHandling(error)),
  postNavigation: (data) =>
    axios
      .post(`/api/navigate`, JSON.stringify(data), {
        headers: {
          "Content-Type": "application/json",
        },
      })
      .catch((error) => errorHandling(error)),
};
