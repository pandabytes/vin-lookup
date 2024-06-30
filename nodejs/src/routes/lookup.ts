import express from 'express';
import { findVin, insertVin } from '../db/vin-queries';
import prismaClient from '../db/prisma-client';
import { Vin, isVinCorrectFormat, validateVin } from '../schemas/vin';
import { findCarPhotoUrl, CarImageryApiError } from '../apis/car-imagery';
import { findVin as findVinVpic, VpicApiError } from '../apis/vpic';

type LookupResponse = Vin & { cached: boolean };

const router = express.Router();

router.get('/:vinNumber', async (req, res) => {
  const vinNumber = req.params['vinNumber'];
  if (!isVinCorrectFormat(vinNumber)) {
    res.status(400);
    res.json({ message: 'VIN must be a 17 alphanumeric characters string.' });
    return;
  }

  const cacheVin = await findVin(prismaClient, vinNumber);
  if (cacheVin) {
    const response: LookupResponse = { ...cacheVin, cached: true };
    res.json(response);
    return;
  }

  try {
    const fetchedVin = await findVinVpic(vinNumber);
    if (!fetchedVin) {
      res.status(404);
      res.json({ message: `VIN "${vinNumber}" not found.` });
      return;
    }

    const photoUrl = await findCarPhotoUrl(fetchedVin.make, fetchedVin.model, fetchedVin.modelYear);
    fetchedVin.photoUrl = photoUrl;
    await insertVin(prismaClient, fetchedVin);

    const response: LookupResponse = { ...fetchedVin, cached: false };
    res.json(response);
  } catch (error) {
    if (error instanceof CarImageryApiError) {
      res.status(503);
      res.json({ message: `CarImagery API returns an error: ${error}.` });
    } else if (error instanceof VpicApiError) {
      res.status(503);
      res.json({ message: `vpic API returns an error: ${error}.` });
    } else {
      res.status(500);
      res.json( { message: `Unexpected error: ${error}.` })
    }
  }
});

export default router;
