import express, { Application, Request, Response } from 'express';
import cors from 'cors';
import { default as listRoutes } from './routes/list-vins';
import { default as lookupRoutes } from './routes/lookup';
import { default as removeRoutes } from './routes/remove-vin';
import prismaClient from './db/prisma-client';

const port = 3001;
const app: Application = express();
app.use(cors()); // https://en.wikipedia.org/wiki/Cross-origin_resource_sharing
app.use(express.json()); // JSON body parser middleware

// Clear the cache each time the app starts
prismaClient.vin.deleteMany().then(count => {});

app.use('/list', listRoutes);
app.use('/lookup', lookupRoutes);
app.use('/remove', removeRoutes);

app.listen(port, (): void => {
  console.log('SERVER IS UP ON PORT:', port);
});
