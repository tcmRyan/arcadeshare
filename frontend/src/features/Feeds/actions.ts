import { IGame } from "../Game/gameSlice";
import { Dispatch, useState } from "react";
import { feedActions, IFeed } from "./feedSlice";
import arcadeAxios from "../../arcadeAxios";
import { AxiosError, AxiosResponse } from "axios";

export const start = () => {
  return (dispatch: Dispatch<any>) => {
    dispatch(feedActions.start());
  };
};
export const addToFeed = (feed: IFeed, game: IGame) => {
  return async (dispatch: Dispatch<any>) => {
    dispatch(feedActions.addGameToCurrent(game));
    await arcadeAxios
      .put(`/api/feeds/${feed.id}`, { ...feed })
      .then((resp: AxiosResponse) => {
        dispatch(feedActions.currentFeedSet(resp.data));
      })
      .catch((e: AxiosError) => {
        console.log(e.message);
      });
  };
};

export const setCurrentFeed = (feed: IFeed | null) => {
  return async (dispatch: Dispatch<any>) => {
    dispatch(feedActions.currentFeedSet(feed));
  };
};

export const updateFeed = (feed: IFeed) => {
  return async (dispatch: Dispatch<any>) => {
    dispatch(feedActions.start());
    await arcadeAxios
      .put(`/api/feeds/${feed.id}`, { ...feed })
      .then((resp: AxiosResponse) => {
        dispatch(feedActions.feedUpdate(resp.data));
      })
      .catch((e: AxiosError) => {
        console.log(e.message);
      });
  };
};

export const createFeed = (feed: IFeed) => {
  return async (dispatch: Dispatch<any>) => {
    dispatch(feedActions.start());
    await arcadeAxios
      .post("/api/feeds", { ...feed })
      .then((resp: AxiosResponse) => {
        dispatch(feedActions.currentFeedSet(resp.data));
      })
      .catch((e) => console.log(e.message));
  };
};

export const removeFromFeed = (game: IGame) => {
  return (dispatch: Dispatch<any>) => {
    dispatch(feedActions.start());
    dispatch(feedActions.removeGameFromCurrent(game));
  };
};

export const fetchFeeds = () => {
  return async (dispatch: Dispatch<any>) => {
    await arcadeAxios
      .get("/api/feeds")
      .then((resp: AxiosResponse) =>
        dispatch(feedActions.feedListFetch(resp.data))
      )
      .catch((e: AxiosError) => {
        dispatch(feedActions.fetchFailed(e.message));
      });
  };
};
