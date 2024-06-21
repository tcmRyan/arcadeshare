import React, { useState } from "react";
import classes from "./SearchBar.module.css";

interface IQueryState {
  query: string;
}

interface ISearchProps {
  onSubmit: Function;
}

const SearchBar = (props: ISearchProps) => {
  const [queryState, setQueryState] = useState<IQueryState>({ query: "" });

  const onSubmit = (event: React.SyntheticEvent) => {
    event.preventDefault();
    const target = event.target as typeof event.target & {
      searchBar: { value: string };
    };
    props.onSubmit(target.searchBar.value);
    setQueryState({ query: "" });
  };

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setQueryState({ query: event.target.value });
  };

  return (
    <div>
      <h3 className={classes.header}>Let's add some games to your feed</h3>
      <form onSubmit={onSubmit} className={classes.searchbar}>
        <label htmlFor="searchBar">Filter Games</label>
        <input
          id="searchBar"
          name="searchBar"
          onChange={handleChange}
          value={queryState.query}
          className={classes.searchbarInput}
        />
        <button type="submit">Search</button>
      </form>
    </div>
  );
};

export default SearchBar;
