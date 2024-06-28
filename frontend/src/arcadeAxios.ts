import axios, { AxiosRequestConfig, AxiosError } from "axios";
import { useAppDispatch } from "./app/hooks";

import { Store } from "@reduxjs/toolkit";
import { logout } from "./features/Auth/actions";

let store: Store;

export const injectStore = (_store: Store) => {
  store = _store;
};

const instance = axios.create();

instance.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    console.log(config);
    if (config.headers) {
      config.headers.Authorization = `Bearer ${
        store.getState().auth.profile.access_token
      }`;
    } else {
      config.headers = {
        Authorization: `Bearer ${store.getState().auth.profile.access_token}`,
      };
    }

    return config;
  },
  (error: AxiosError) => {
    const dispatch = useAppDispatch();
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      localStorage.removeItem("expirationDate");
      dispatch(logout());
    }
    return Promise.reject(error);
  }
);

export default instance;
