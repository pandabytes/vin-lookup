import express, { Application, Request, Response } from 'express';
import cors from 'cors';
import { Vin, validate } from './schemas/vin'
import { PrismaClient } from '@prisma/client'
import { getAllvins, insertVin } from './db/vin-queries';

const port = 3001;
const app: Application = express();
app.use(cors()); // https://en.wikipedia.org/wiki/Cross-origin_resource_sharing
app.use(express.json()); // JSON body parser middleware

// No need to explictly disconnect prisma as stated in
// https://www.prisma.io/docs/orm/prisma-client/setup-and-configuration/databases-connections#prismaclient-in-long-running-applications
const prismaClient = new PrismaClient();

// Clear the cache each time the app starts
prismaClient.vin.deleteMany().then(count => {});

const vin: Vin = validate({
  vinNumber: '12345678901234567',
  make: 'x',
  model: 'x',
  modelYear: 'x',
  bodyClass: 'x',
  photoUrl: undefined
});

// console.log(vin);
// console.log(validate(vin))

// insertVin(prismaClient, vin)
//   .then(_ => {
//     getAllvins(prismaClient).then(result => console.log(result));
//   });
// getAllvins(prismaClient).then(result => console.log(result));

// const server = app.listen(port, (): void => {
//   console.log('SERVER IS UP ON PORT:', port);
// });
