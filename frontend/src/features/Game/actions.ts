import { GameFormValues } from "./GameForm/GameForm";
import { Dispatch } from "react";
import arcadeAxios from "../../arcadeAxios";
import { AxiosError, AxiosResponse } from "axios";
import { gameActions, IGame } from "./gameSlice";

export const updateThumbnail = (id: number, thumbnail: File) => {
  return async (dispatch: Dispatch<any>) => {
    dispatch(gameActions.start());
    let formData = new FormData();
    formData.append("thumbnail", thumbnail);
    await arcadeAxios
      .put(`/api/games/${id}`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      .then((resp: AxiosResponse<any>) => {
        dispatch(gameActions.thumbnailSuccess(resp.data));
      });
  };
};

const createFormData = (gameData: GameFormValues) => {
  let formData = new FormData();
  if (gameData.upload) {
    formData.append("upload", gameData.upload);
  }
  if (gameData.thumbnail) {
    formData.append("thumbnail", gameData.thumbnail);
  }
  formData.append("name", gameData.name);
  formData.append("description", gameData.description);
  return formData;
};

export const createGame = (gameData: GameFormValues) => {
  return async (dispatch: Dispatch<any>) => {
    dispatch(gameActions.start());
    const formData = createFormData(gameData);
    console.log("Creating Game");
    console.log(formData);

    await arcadeAxios
      .post("/api/games", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      .then((resp: AxiosResponse<any>) => {
        dispatch(gameActions.success(resp.data));
      })
      .catch((error: AxiosError) => {
        dispatch(gameActions.failure(error.message));
      });
  };
};

export const updateGame = (gameData: GameFormValues) => {
  return async (dispatch: Dispatch<any>) => {
    dispatch(gameActions.start());
    let formData = createFormData(gameData);
    await arcadeAxios
      .put(`/api/games/${gameData.id}`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      .then((resp: AxiosResponse) => {
        dispatch(gameActions.success(resp.data));
      })
      .catch((error: AxiosError) => {
        dispatch(gameActions.failure(error.message));
      });
  };
};

export const selectGame = (game: IGame) => {
  return (dispatch: Dispatch<any>) => {
    dispatch(gameActions.selectGame(game));
  };
};

export const cleanGame = () => {
  return (dispatch: Dispatch<any>) => {
    dispatch(gameActions.cleanGame());
  };
};

export const fetchGames = () => {
  return async (dispatch: Dispatch<any>) => {
    dispatch(gameActions.start());
    await arcadeAxios
      .get("/api/games")
      .then((resp: AxiosResponse) => {
        dispatch(gameActions.gamesSuccess(resp.data));
      })
      .catch((error: AxiosError) => {
        dispatch(gameActions.failure(error.message));
      });
  };
};
