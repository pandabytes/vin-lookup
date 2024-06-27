import { useEffect, useState } from 'react';
import Header from './Components/Header';
import SearchVin from './Components/SearchVin';
import ExportVins from './Components/ExportVins';
import VinsTable from './Components/VinsTable';

import { Vin } from './types';

const API_URL = 'http://localhost:8000';

async function lookupVin(vin: string): Promise<Vin> {
  const url = `${API_URL}/lookup/${vin}`;
  const response = await fetch(url, { method: 'GET' });
  if (!response.ok) {
    throw new Error(`VIN lookup api returned with a ${response.statusText}.`);
  }
  
  const json = await response.json();
  return mapToVinObject(json);
}

async function listVins(): Promise<Array<Vin>> {
  const url = `${API_URL}/list`;
  const response = await fetch(url, { method: 'GET' });
  if (!response.ok) {
    throw new Error(`VIN lookup api returned with a ${response.statusText}.`);
  }
  
  const json = await response.json();
  return json.vins.map(mapToVinObject);
}

async function exportVins(export_format: string = 'csv'): Promise<void> {
  const url = `${API_URL}/export?export_format=${export_format}`;
  const response = await fetch(url, { method: 'GET' });
  if (!response.ok) {
    throw new Error(`VIN lookup api returned with a ${response.statusText}.`);
  }

  const blob = await response.blob();
  const urlBlob = URL.createObjectURL(blob);
  const anchorElement = document.createElement('a');
  anchorElement.href = urlBlob;
  anchorElement.download = `vins.${export_format}` ?? '';
  anchorElement.click();
  anchorElement.remove();
  URL.revokeObjectURL(url);
}

function mapToVinObject(vinJson: { [key: string]: string }): Vin {
  return {
    vinNumber: vinJson.vin,
    make: vinJson.make,
    model: vinJson.model,
    modelYear: vinJson.model_year,
    bodyClass: vinJson.body_class,
    photoUrl: vinJson.photo_url,
  }
}

export default function App() {
  const [cachedVins, setCachedVins] = useState(new Set<string>());
  const [vins, setVins] = useState<Array<Vin>>([]);

  async function handleSearchClicked(vinNumber: string): Promise<void> {
    if (cachedVins.has(vinNumber)) {
      return;
    }

    try {
      const vin = await lookupVin(vinNumber);
      const vinsCopy = vins.slice();
      vinsCopy.push(vin);
      setVins(vinsCopy);

      const cachedVinsCopy = new Set(cachedVins);
      cachedVinsCopy.add(vin.vinNumber);
      setCachedVins(cachedVinsCopy);
    } catch (error) {
      alert(error);
    }
  }

  async function handleExportClicked(exportFormat: string): Promise<void> {
    try {
      await exportVins(exportFormat);
    } catch (error) {
      alert(`Failed to export vins: ${error}.`)
    }
  }

  // Initially load the vins
  useEffect(() => {
    listVins()
      .then(vinsFromApi => {
        const vinsCopy = vins.slice();
        const cachedVinsCopy = new Set(cachedVins);

        for (const vin of vinsFromApi) {
          vinsCopy.push(vin);
          cachedVinsCopy.add(vin.vinNumber);
        }

        setVins(vinsCopy);
        setCachedVins(cachedVinsCopy);
      })
      .catch(error => alert(`Failed to fetch VINs: ${error}.`));
  }, []);

  return (
    <>
      <Header />
      <SearchVin onSearchClicked={handleSearchClicked} />
      <br />
      <ExportVins onExportClicked={handleExportClicked} />
      <VinsTable vins={vins} />
    </>
  );
}
