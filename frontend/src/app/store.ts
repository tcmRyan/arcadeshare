import { configureStore, ThunkAction, Action } from "@reduxjs/toolkit";

import AuthSlice from "../features/Auth/AuthSlice";
import AdminSlice from "../features/Admin/AdminSlice";
import GameSlice from "../features/Game/gameSlice";
import FeedSlice from "../features/Feeds/feedSlice";

export const store = configureStore({
  reducer: {
    auth: AuthSlice.reducer,
    admin: AdminSlice.reducer,
    game: GameSlice.reducer,
    feed: FeedSlice.reducer,
  },
});

export default store;

export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;
