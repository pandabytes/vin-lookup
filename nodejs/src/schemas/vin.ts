import { z } from 'zod';

// https://dev.to/isnan__h/custom-schema-validation-in-typescript-with-zod-5cp5
// https://github.com/colinhacks/zod/issues/37

export type Vin = z.infer<typeof VinSchema>;

export function validate(vin: Vin) {
  return VinSchema.parse(vin);
}

export function isVinCorrectFormat(vinNumber: string): boolean {
  return vinNumber.length === 17 && isAlphaNumeric(vinNumber);
}

const VinSchema = z.object({
  vin: z.string({})
    .transform((value, _) => value.trim().toUpperCase())
    .refine(isVinCorrectFormat,
            value => ({ message: `"VIN ${value}" must be a 17 alphanumeric characters string.`})),
  make: z.string()
    .transform((value, _) => value.trim())
    .refine(isNotEmpty, getEmptyStringMessage),
  model: z.string()
    .transform((value, _) => value.trim())
    .refine(isNotEmpty, getEmptyStringMessage),
  modelYear: z.string()
    .transform((value, _) => value.trim())
    .refine(isNotEmpty),
  bodyClass: z.string()
    .transform((value, _) => value.trim())
    .refine(isNotEmpty, getEmptyStringMessage),
  photoUrl: z.string().url().optional(),
});

function isAlphaNumeric(str: string): boolean {
  for (let i = 0; i < str.length; i++) {
    const code = str.charCodeAt(i);
    if (!(code > 47 && code < 58) && // numeric (0-9)
        !(code > 64 && code < 91) && // upper alpha (A-Z)
        !(code > 96 && code < 123)) { // lower alpha (a-z)
      return false;
    }
  }
  return true;
};

function isNotEmpty(str: string) {
  return str !== '' && str !== null && str !== undefined;
}

function getEmptyStringMessage(_: string) {
  return { message: `Value must not be an empty string.`};
}
