import { useState } from "react";
import Home from "./pages/Home";
import SearchResults from "./pages/SearchResults";

import "./index.css";


function App() {
  const [view, setView] = useState("home");
  const [inventionDescription, setInventionDescription] = useState("");
  const [results, setResults] = useState([]);

  const handleSearchSubmit = async (invention_description) => {
    setInventionDescription(invention_description);

    const response = await fetch("/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({invention_description: invention_description})
    });

    if (!response.ok) {
      console.error("Error fetching search results:", response.statusText);
      return;
    }
    const data = await response.json();
    setResults(data.results);
    setView("searchResults");
  }
  return (
    view === "home" ? 
      <Home onSubmit={handleSearchSubmit} /> :
      <SearchResults 
        inventionDescription={inventionDescription} 
        results={results} 
      />
  );
}

export default App;
