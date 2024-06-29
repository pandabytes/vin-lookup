import { InvalidArgumentError } from '../errors/argument-error';
import xmldoc from 'xmldoc';

export class CarImageryApiError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'CarImageryApiError';
  }
}

export async function findCarPhotoUrl(make: string, model: string, modelYear: string): Promise<string | null> {
  [make, model, modelYear] = make.trim(), model.trim(), modelYear.trim();

  if (make === '' || model === '' || modelYear === '') {
    throw new InvalidArgumentError('All arguments must not be empty string and not contain only whitespaces.');
  }

  const searchTerm = `${make} ${model} ${modelYear}`;

  const url = `https://www.carimagery.com/api.asmx/GetImageUrl?searchTerm=${searchTerm}`;
  const response = await fetch(url, { 
    method: 'GET',
    headers: { "Content-Type": "application/xml",
    },
  });

  if (!response.ok) {
    throw new CarImageryApiError(`Failed to get photo url from CarImagery API. Status ${response.status} received.`);
  }

  // Expect the payload to look like this
  //   <?xml version="1.0" encoding="utf-8"?>
  //   <string xmlns="http://carimagery.com/">http://www.regcheck.org.uk/image.aspx/@dCBvIHk=</string>
  const responseText = await response.text();
  const document = new xmldoc.XmlDocument(responseText);
  return document.val;
}
