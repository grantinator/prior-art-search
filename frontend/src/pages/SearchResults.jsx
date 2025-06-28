// SearchResults.jsx
export default function SearchResults({ inventionDescription, results }) {
    return (
      <div>
        <h1>Patent Prior Art Search Results</h1>
        <br />
  
        <h2>Your invention:</h2>
        <p>{inventionDescription}</p>
  
        <h2>Potential Prior Art</h2>
        {results && results.length > 0 ? (
          results.map((result, index) => (
            <div key={index}>
              <a href={result.unified_patents_link}>
                <h3>
                  <strong>Title: </strong>
                  {result.title}
                </h3>
              </a>
              <p>
                <strong>Abstract: </strong>
                <br />
                {result.abstract}
              </p>
              <p>
                <strong>Similarity:</strong> {result.similarity}
              </p>
            </div>
          ))
        ) : (
          <p>No prior art found for your invention description.</p>
        )}
  
        <a href="/">Search Again</a>
      </div>
    );
  }
  