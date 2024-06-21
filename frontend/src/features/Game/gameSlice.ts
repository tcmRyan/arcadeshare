import { createSlice, current, PayloadAction } from "@reduxjs/toolkit";

export interface IGame {
  id?: number;
  name: string;
  description: string;
  bucket: string;
  thumbnail: string;
  version: string;
  thumbnail_uri: string;
  game_uri: string;
  owner_id: number;
}

interface IGameState {
  game: IGame | null;
  games: IGame[];
  loading: boolean;
  loaded: boolean;
  error: string;
}

const initialState: IGameState = {
  game: null,
  games: [],
  loading: false,
  loaded: false,
  error: "",
};

export const Index = createSlice({
  name: "game",
  initialState,
  reducers: {
    start(state) {
      const currentState = current(state);
      return {
        ...currentState,
        loading: true,
        error: "",
      };
    },
    gamesSuccess(state, action: PayloadAction<IGame[]>) {
      const currentState = current(state);
      return {
        ...currentState,
        loading: false,
        loaded: true,
        error: "",
        games: action.payload,
      };
    },
    success(state, action: PayloadAction<IGame>) {
      const currentState = current(state);
      const updatedGames = currentState.games.map((game, i) =>
        game.id === action.payload.id ? action.payload : game
      );
      return {
        ...currentState,
        loading: false,
        error: "",
        game: null,
        games: updatedGames,
      };
    },
    thumbnailSuccess(state, action: PayloadAction<IGame>) {
      const currentState = current(state);
      const updatedGames = currentState.games.map((game, i) =>
        game.id === action.payload.id ? action.payload : game
      );

      return {
        ...currentState,
        games: updatedGames,
      };
    },
    failure(state, action: PayloadAction<string>) {
      const currentState = current(state);
      return {
        ...currentState,
        error: action.payload,
      };
    },
    selectGame(state, action: PayloadAction<IGame>) {
      const currentState = current(state);
      return {
        ...currentState,
        game: action.payload,
      };
    },
    cleanGame(state) {
      state.game = null;
    },
  },
});

export const gameActions = Index.actions;
export default Index;
