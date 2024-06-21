import { createSlice, current, PayloadAction } from "@reduxjs/toolkit";
import { Profile } from "../../app/types";

interface IAuthState {
  profile: Profile | null;
  error: string | null;
  authenticated: boolean;
  checked: boolean;
  vendorUrl: string;
}

const initialState: IAuthState = {
  authenticated: false,
  checked: false,
  error: "",
  profile: null,
  vendorUrl: "",
};

export const Index = createSlice({
  name: "auth",
  initialState,
  reducers: {
    start(state, action: PayloadAction<string>) {
      state.vendorUrl = action.payload;
    },

    success(state, action: PayloadAction<Profile>) {
      const currentState = current(state);
      return {
        ...currentState,
        authenticated: true,
        checked: true,
        profile: action.payload,
        vendorUrl: "",
        error: "",
      };
    },

    logout(state) {
      return { ...initialState, checked: true };
    },
  },
});

export const authActions = Index.actions;
export default Index;
