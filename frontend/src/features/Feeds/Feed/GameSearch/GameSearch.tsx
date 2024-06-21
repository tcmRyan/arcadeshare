import SearchBar from "components/UI/SearchBar/SearchBar";
import React, { useCallback, useEffect, useState } from "react";
import arcadeAxios from "arcadeAxios";
import { AxiosResponse } from "axios";
import { IGame } from "features/Game/gameSlice";
import SearchGrid from "components/UI/SearchGrid/SearchGrid";

const GameSearch = () => {
  interface ISearchState {
    results: IGame[];
    loaded: boolean;
  }

  const [searchState, setSearchState] = useState<ISearchState>({
    results: [],
    loaded: false,
  });

  const searchGames = useCallback(async (query: string = "") => {
    const data = await arcadeAxios
      .get("/api/games/search", { params: { query: query } })
      .then((resp: AxiosResponse) => {
        return resp.data;
      })
      .catch((e) => {
        console.log(e.message);
        return [];
      });
    setSearchState({ loaded: true, results: data });
  }, []);

  useEffect(() => {
    if (searchState.results.length === 0 && !searchState.loaded) {
      setSearchState({ results: [], loaded: true });
      searchGames().catch(console.error);
    }
  }, [searchState, searchGames]);

  return (
    <div>
      <SearchBar onSubmit={searchGames} />
      <SearchGrid games={searchState.results} />
    </div>
  );
};

export default GameSearch;
