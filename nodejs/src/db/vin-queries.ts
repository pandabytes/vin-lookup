import { PrismaClient, Vin as VinEntity } from '@prisma/client'
import { Vin as VinSchema } from '../schemas/vin'

export async function getAllvins(prismaClient: PrismaClient): Promise<Array<VinSchema>> {
  const vins = await prismaClient.vin.findMany();
  return vins.map(mapToVinSchema);
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

export async function findVin(prismaClient: PrismaClient, vinNumber: string): Promise<VinSchema | null> {
  const vinEntity = await prismaClient.vin.findUnique({ where: { vinNumber: vinNumber } });
  if (!vinEntity) {
    return null;
  }

  return mapToVinSchema(vinEntity);
}

export async function removeVin(prismaClient: PrismaClient, vinNumber: string): Promise<boolean> {
  const deletedVins = await prismaClient.vin.deleteMany({ where: { vinNumber: vinNumber }});
  return deletedVins.count > 0;
}

function mapToVinSchema(vinEntity: VinEntity): VinSchema {
  const vinSchema: VinSchema = {
    vinNumber: vinEntity.vinNumber,
    make: vinEntity.make,
    model: vinEntity.model,
    modelYear: vinEntity.modelYear,
    bodyClass: vinEntity.bodyClass,
  };

  if (vinEntity.photoUrl) {
    vinSchema.photoUrl = vinEntity.photoUrl;
  }

  return vinSchema;
}
