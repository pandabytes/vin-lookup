import { useEffect, useState } from 'react';
import Header from './Components/Header';
import SearchVin from './Components/SearchVin';
import ExportVins from './Components/ExportVins';
import VinsTable from './Components/VinsTable';

const API_URL = 'http://localhost:8000';

async function lookupVin(vin) {
  const url = `${API_URL}/lookup/${vin}`;
  const response = await fetch(url, { method: 'GET', 'content-type': 'application/json' });
  if (!response.ok) {
    throw new Error(`VIN lookup api returned with a ${response.statusText}.`);
  }
  return await response.json();
}

async function listVins() {
  const url = `${API_URL}/list`;
  const response = await fetch(url, { method: 'GET', 'content-type': 'application/json' });
  if (!response.ok) {
    throw new Error(`VIN lookup api returned with a ${response.statusText}.`);
  }
  return await response.json();
}

async function exportVins(export_format = 'csv') {
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

function mapToVinObject(vinJson) {
  return {
    vin: vinJson.vin,
    make: vinJson.make,
    model: vinJson.model,
    modelYear: vinJson.model_year,
    bodyClass: vinJson.body_class,
    photoUrl: vinJson.photo_url,
  }
}

export default function App() {
  const [cachedVins, setCachedVins] = useState(new Set());
  const [vins, setVins] = useState([]);

  function handleSearchClicked(vinNumber) {
    if (cachedVins.has(vinNumber)) {
      return;
    }

    lookupVin(vinNumber)
      .then(vinJson => {
        const vinsCopy = vins.slice();
        vinsCopy.push(mapToVinObject(vinJson));
        setVins(vinsCopy);
        
        const cachedVinsCopy = new Set(cachedVins);
        cachedVinsCopy.add(vinJson.vin);
        setCachedVins(cachedVinsCopy);
      })
      .catch(error => alert(error));
  }

  function handleExportClicked(exportFormat) {
    exportVins(exportFormat)
      .catch(error => alert(`Failed to export vins: ${error}.`));
  }

  // Initially load the vins
  useEffect(() => {
    listVins()
      .then(vinsJson => {
        const vinsCopy = vins.slice();
        const cachedVinsCopy = new Set(cachedVins);

        for (const vinJson of vinsJson.vins) {
          vinsCopy.push(mapToVinObject(vinJson));
          cachedVinsCopy.add(vinJson.vin);
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
