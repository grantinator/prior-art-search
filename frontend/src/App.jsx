import { useState } from "react";
import Home from "./pages/Home";
import SearchResults from "./pages/SearchResults";

import "./index.css";


function App() {
  const [view, setView] = useState("home");
  const [inventionDescription, setInventionDescription] = useState("");
  const [results, setResults] = useState([]);
  const [error, setError] = useState("");

  const handleSearchSubmit = async (invention_description) => {
    setInventionDescription(invention_description);

    try {
      const response = await fetch("/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({invention_description: invention_description})
      });
      if (!response.ok) {
        if (response.status === 404) {
          setError("No similar patents found for your invention description.");
          setView("error");
        } else {
          console.error("Error fetching search results:", response.statusText);
          setError("Something went wrong. Please try again.");
          setView("error");
        }
        return
      }
      const data = await response.json();
      setResults(data.results);
      setView("searchResults");
    } catch (err) {
      setError("Failed to fetch search results. Please try again.");
      setView("error");
    }
  }
  return (
    <>
    {view == "home" && (
      <Home onSubmit={handleSearchSubmit} /> 
    )}
    {view === "searchResults" && (
      <SearchResults 
        inventionDescription={inventionDescription} 
        results={results} 
      />
    )}
    {view === "error" && (
      <div>
        <h1>Error</h1>
        <p>{error}</p>
        <button onClick={() => setView("home")}>Go Back</button>
      </div>
    )}
    </>
  );
}

export default App;
