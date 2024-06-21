import { Dispatch } from "react";
import arcadeAxios from "../../arcadeAxios";
import { AxiosError } from "axios";
import { adminActions } from "./AdminSlice";
import { Role } from "../../app/types";

interface INewUser {
  username: string;
  password: string;
  email: string | null;
  roles: Role[];
}

export const getUsers = () => {
  return async (dispatch: Dispatch<any>) => {
    await arcadeAxios
      .get("/api/users")
      .then((response) => {
        dispatch(adminActions.success(response.data));
      })
      .catch((error: AxiosError) => {
        console.log(error);
      });
  };
};

export const getRoles = () => {
  return async (dispatch: Dispatch<any>) => {
    await arcadeAxios
      .get("/api/roles/")
      .then((response) => {
        dispatch(adminActions.updateRoles(response.data));
      })
      .catch((error: AxiosError) => {
        console.log(error);
      });
  };
};

export const createUser = (userData: INewUser) => {
  return async (dispatch: Dispatch<any>) => {
    let config = {
      headers: {
        "Content-Type": "application/json",
      },
    };
    await arcadeAxios
      .post("/api/users", userData, config)
      .then((response) => {
        dispatch(adminActions.updateUsers(response.data));
      })
      .catch((error: AxiosError) => {
        console.log(error);
      });
  };
};
