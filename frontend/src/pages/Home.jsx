// Home.jsx
import { useState } from "react";

export default function Home({ onSubmit }) {
  const [inventionDescription, setInventionDescription] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(inventionDescription);
  };

  return (
    <div>
      <header>
        <div className="logo">
          <h1>
            Patent.<span style={{ opacity: 0.5 }}>ly</span>
          </h1>
        </div>
        <div className="nav">
          <button>Demo</button>
          <button>About</button>
          <button>Contact</button>
        </div>
      </header>

      <div className="primary-content">
        <div className="title">
          <h1>Find Prior Art in Seconds</h1>
        </div>
        <p>AI powered search to find patents related to your ideas.</p>

        <form onSubmit={handleSubmit}>
          <textarea
            id="invention_description"
            name="invention_description"
            placeholder="Describe your invention..."
            value={inventionDescription}
            onChange={(e) => setInventionDescription(e.target.value)}
            required
          />
          <br />
          <input type="submit" value="Search" />
        </form>
      </div>
    </div>
  );
}
