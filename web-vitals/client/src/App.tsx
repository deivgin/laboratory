import { useEffect, useState } from "react";

type ApiData = Array<{
  id: number;
  title: string;
}>;

function App() {
  const [data, setData] = useState<ApiData | undefined>(undefined);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("http://localhost:3001/api/data")
      .then((res) => res.json())
      .then((data: ApiData) => {
        setData(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching data:", err);
        setError("Failed to load data");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <>Loading...</>;
  }

  if (error) {
    return <>{error}</>;
  }

  return (
    <ul>
      {data?.map((x) => (
        <li key={x.id}>{x.title}</li>
      ))}
    </ul>
  );
}

export default App;
