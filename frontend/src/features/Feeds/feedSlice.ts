import { createSlice, current, PayloadAction } from "@reduxjs/toolkit";
import { IGame } from "../Game/gameSlice";

export interface IFeed {
  id?: number;
  name: string;
  owner_id: number;
  description: string;
  games: IGame[];
}

interface IFeedState {
  current: IFeed | null;
  feeds: IFeed[];
  loading: boolean;
  loaded: boolean;
  error: string;
}

const initialState: IFeedState = {
  current: null,
  feeds: [],
  loading: false,
  loaded: false,
  error: "",
};

export const Index = createSlice({
  name: "feed",
  initialState,
  reducers: {
    start(state) {
      const currentState = current(state);
      return {
        ...currentState,
        loading: true,
        loaded: false,
        error: "",
      };
    },
    feedListFetch(state, action: PayloadAction<IFeed[]>) {
      const currentState = current(state);
      return {
        ...currentState,
        loading: false,
        loaded: true,
        feeds: action.payload,
      };
    },
    currentFeedSet(state, action: PayloadAction<IFeed | null>) {
      const currentState = current(state);
      return {
        ...currentState,
        loading: false,
        loaded: true,
        current: action.payload,
      };
    },
    feedUpdate(state, action: PayloadAction<IFeed>) {
      const currentState = current(state);
      const updatedFeedList = currentState.feeds.map((feed) =>
        feed.id === action.payload.id ? action.payload : feed
      );
      return {
        ...currentState,
        feeds: updatedFeedList,
        current: action.payload,
        loaded: true,
        loading: false,
      };
    },
    feedListUpdate(state, action: PayloadAction<IFeed>) {
      const currentState = current(state);
      const updatedFeedList = currentState.feeds.map((feed, i) =>
        feed.id === action.payload.id ? action.payload : feed
      );
      return {
        ...currentState,
        feeds: updatedFeedList,
      };
    },
    addGameToCurrent(state, action: PayloadAction<IGame>) {
      const currentState = current(state);
      if (currentState.current) {
        let games = [...currentState.current.games];
        games.push(action.payload);
        const currentFeed: IFeed = { ...currentState.current, games: games };
        const updatedFeedList = currentState.feeds.map((feed, i) =>
          feed.id === currentFeed.id ? currentFeed : feed
        );
        return {
          ...currentState,
          current: currentFeed,
          feeds: updatedFeedList,
          loading: false,
          loaded: true,
        };
      }
    },
    removeGameFromCurrent(state, action: PayloadAction<IGame>) {
      const currentState = current(state);
      if (currentState.current) {
        const gameList = currentState.current.games.filter(
          (game) => game.id !== action.payload.id
        );
        const currentFeed: IFeed = { ...currentState.current, games: gameList };
        const updatedFeedList = currentState.feeds.map((feed, i) =>
          feed.id === currentFeed.id ? currentFeed : feed
        );
        return {
          ...currentState,
          current: currentFeed,
          loading: false,
          loaded: true,
          feeds: updatedFeedList,
        };
      }
    },
    fetchFailed(state, action: PayloadAction<string>) {
      state.error = action.payload;
    },
    feedClear(state) {
      state.current = null;
    },
  },
});

export const feedActions = Index.actions;
export default Index;
