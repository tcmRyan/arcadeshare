import { createSlice, current, PayloadAction } from "@reduxjs/toolkit";
import { Role, User } from "../../app/types";

interface IAdminState {
  users: Array<User>;
  roles: Array<Role>;
  error: string | null;
  loading: boolean;
}

const initialState: IAdminState = {
  users: [],
  roles: [],
  error: "",
  loading: false,
};

export const Index = createSlice({
  name: "admin",
  initialState,
  reducers: {
    start(state) {
      const currentState = current(state);
      return {
        ...currentState,
        loading: true,
      };
    },
    success(state, action: PayloadAction<Array<User>>) {
      const currentState = current(state);
      return {
        ...currentState,
        users: action.payload,
      };
    },
    updateRoles(state, action: PayloadAction<Array<Role>>) {
      const currentState = current(state);
      return {
        ...currentState,
        roles: action.payload,
      };
    },
    updateUsers(state, action: PayloadAction<User>) {
      const currentState = current(state);
      const users = state.users;
      users.push(action.payload);
      return {
        ...currentState,
        users: users,
      };
    },
  },
});

export const adminActions = Index.actions;
export default Index;
