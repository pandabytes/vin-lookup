import express from 'express';
import { getAllvins } from '../db/vin-queries';
import prismaClient from '../db/prisma-client';

const router = express.Router();

router.get('/', async (req, res) => {
  const vins = await getAllvins(prismaClient);
  res.json({ vins });
});

export default router;
