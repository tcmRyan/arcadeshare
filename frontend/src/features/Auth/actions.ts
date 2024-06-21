import { Dispatch } from "react";
import { authActions } from "./AuthSlice";
import axios, { AxiosError } from "axios";
import loginTab from "./loginTab";
import { Profile } from "../../app/types";

export const basicLogin = (username: string, password: string) => {
  return async (dispatch: Dispatch<any>) => {
    await axios
      .post("/auth/user-login", { username: username, password: password })
      .then((response) => {
        const data = response.data;
        updateStorage(data);
        dispatch(authActions.success(data));
      })
      .catch((error: AxiosError) => {
        console.log(error);
        return {};
      });
  };
};
export const oauthLogin = (vendorUrl: string) => {
  return async (dispatch: Dispatch<any>) => {
    const fetch = async () => {
      const msg = loginTab(vendorUrl);
      const msgData = await msg
        .then((data) => {
          updateStorage(data);
          return data;
        })
        .catch((error: AxiosError) => {
          console.log(error);
          return {};
        });
      return msgData;
    };
    const data = await fetch();
    dispatch(checkTimeout(data.expires_in));
    dispatch(authActions.success(data));
  };
};
export const logout = () => {
  return async (dispatch: Dispatch<any>) => {
    localStorage.removeItem("token");
    localStorage.removeItem("expirationDate");
    dispatch(authActions.logout());
  };
};

const updateStorage = (data: Profile) => {
  const expirationDate = new Date(
    new Date().getTime() + data.expires_in * 1000
  );
  localStorage.setItem("token", data.access_token);
  localStorage.setItem("expirationDate", expirationDate.toLocaleString());
};

export const checkTimeout = (expirationTime: number) => {
  return (dispatch: Dispatch<any>) => {
    setTimeout(() => {
      console.log("token expired");
      dispatch(logout());
    }, expirationTime * 1000);
  };
};

export const checkState = () => {
  return async (dispatch: Dispatch<any>) => {
    const token = localStorage.getItem("token");
    const expires = localStorage.getItem("expirationDate");
    let expirationDate = expires ? new Date(expires) : new Date();
    if (!token || expirationDate <= new Date()) {
      dispatch(logout());
    } else {
      const authHeader = `Bearer ${token}`;
      axios
        .get("/api/users/me", { headers: { Authorization: authHeader } })
        .then((resp) => {
          dispatch(authActions.success(resp.data));
          expirationDate = new Date(
            new Date().getTime() + resp.data.expires_in * 1000
          );
          updateStorage(resp.data);
          const timeout =
            expirationDate.getTime() - new Date().getTime() / 1000;
          dispatch(checkTimeout(timeout));
        })
        .catch((error) => {
          console.log(error);
        });
    }
  };
};
