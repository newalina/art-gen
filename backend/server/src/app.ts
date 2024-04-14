import express from "express";
import dotenv from "dotenv";
import { Request, Response } from "express";
import { NodeRouter } from "./nodes";
import cors from "cors";
import { MongoClient } from "mongodb";

dotenv.config();
const PORT = process.env.PORT;

const app = express();

// start the express web server listening on 8000
app.listen(PORT, () => {
  console.log("Server started on port", PORT);
});

app.use(cors());
app.use(express.static("dist"));
app.use(express.json());

const uri = process.env.DB_URI;
const mongoClient = new MongoClient(uri, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});
mongoClient.connect().then(() => {
  console.log("Connected to MongoDB");
});
// node router
const myNodeRouter = new NodeRouter(mongoClient);
app.use("/node", myNodeRouter.getExpressRouter());

app.get("*", (req: Request, res: Response) => {
  res.send("Art-Gen");
});
