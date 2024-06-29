import express, { Application, Request, Response } from 'express';
import cors from 'cors';

const port = 3001;
const app: Application = express();
app.use(cors()); // https://en.wikipedia.org/wiki/Cross-origin_resource_sharing
app.use(express.json()); // JSON body parser middleware


app.listen(port, (): void => {
  console.log('SERVER IS UP ON PORT:', port);
});
