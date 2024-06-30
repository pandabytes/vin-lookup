import express from 'express';
import { removeVin } from '../db/vin-queries';
import prismaClient from '../db/prisma-client';
import { isVinCorrectFormat } from '../schemas/vin';

const router = express.Router();

type RemoveResponse = {
  vinNumber: string;
  cacheDeleteSuccess: boolean;
}

router.delete('/:vinNumber', async (req, res) => {
  const vinNumber = req.params['vinNumber'];
  if (!isVinCorrectFormat(vinNumber)) {
    res.status(400);
    res.json({ message: 'VIN must be a 17 alphanumeric characters string.' });
    return;
  }

  const vinRemoved = await removeVin(prismaClient, vinNumber);
  const response: RemoveResponse = { vinNumber, cacheDeleteSuccess: vinRemoved };
  res.json(response);
});

export default router;
