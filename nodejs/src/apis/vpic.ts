import { InvalidArgumentError } from '../errors/argument-error';
import { Vin, isVinCorrectFormat, validateVin } from '../schemas/vin';

export class VpicApiError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'CarImageryApiError';
  }
}

export async function findVin(vinNumber: string): Promise<Vin | null> {
  if (!isVinCorrectFormat(vinNumber)) {
    throw new InvalidArgumentError(`VIN ${vinNumber} must be a 17 alphanumeric characters string.`)
  }

  const url = `https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/${vinNumber}?format=json`;
  const response = await fetch(url, { method: 'GET' });

  if (!response.ok) {
    throw new VpicApiError(`Failed to get VIN ${vinNumber} from vpic API. Status ${response.status} received.`);
  }

  const payload = (await response.json())['Results'][0];
  try {
    return validateVin({
      vinNumber: vinNumber,
      make: payload['Make'],
      model: payload['Model'],
      modelYear: payload['ModelYear'],
      bodyClass: payload['BodyClass'],
    });
  } catch (error) {
    return null;
  }
}
