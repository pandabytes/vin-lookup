import { PrismaClient } from '@prisma/client'
import { Vin as VinSchema } from '../schemas/vin'

export async function getAllvins(prismaClient: PrismaClient): Promise<Array<VinSchema>> {
  const vins = await prismaClient.vin.findMany();
  return vins.map(vin => {
    const vinSchema: VinSchema = {
      vinNumber: vin.vinNumber,
      make: vin.make,
      model: vin.model,
      modelYear: vin.modelYear,
      bodyClass: vin.bodyClass,
    };

    if (vin.photoUrl) {
      vinSchema.photoUrl = vin.photoUrl;
    }

    return vinSchema;
  });
}

export async function insertVin(prismaClient: PrismaClient, vin: VinSchema): Promise<void> {
  await prismaClient.vin.create({
    data: {
      vinNumber: vin.vinNumber,
      make: vin.make,
      model: vin.model,
      modelYear: vin.modelYear,
      bodyClass: vin.bodyClass,
      photoUrl: vin.photoUrl,
    }
  });
}
