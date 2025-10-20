import express, { Request, Response } from "express";
import cors from "cors";

const app = express();
const PORT = 3001;

app.use(cors());
app.use(express.json());

type ApiDataDto = Array<{
  id: number;
  title: string;
}>;

const DATA_ITEM_COUNT = 1000;

// Simple API endpoint
app.get("/api/data", (req: Request, res: Response) => {
  const response: ApiDataDto = [];

  for (let i = 0; i < DATA_ITEM_COUNT; i++) {
    response.push({ id: i + 1, title: `Data item ${i + 1}` });
  }

  res.json(response);
});

app.listen(PORT, () => {
  console.log(`Backend server running on http://localhost:${PORT}`);
});
