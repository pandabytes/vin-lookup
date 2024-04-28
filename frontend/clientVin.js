const form = document.querySelector('.vin-lookup-form'); // 'form' is tagname
// const loadingElement = document.querySelector('.loading'); // '.loading' is class
const API_URL = 'http://localhost:8000';

const cachedVins = new Map()

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

function addVinToTable(vinJson) {
  const table = document.querySelector('.vins');
  const row = table.insertRow(0);
  
  const vinCell = row.insertCell(0);
  const makeCell = row.insertCell(1);
  const modelCell = row.insertCell(2);
  const modelYearCell = row.insertCell(3);
  const bodyClassCell = row.insertCell(4);
  const photoCell = row.insertCell(5);

  vinCell.innerHTML = vinJson.vin;
  makeCell.innerHTML = vinJson.make;
  modelCell.innerHTML = vinJson.model;
  modelYearCell.innerHTML = vinJson.model_year;
  bodyClassCell.innerHTML = vinJson.body_class;

  const imgId = `img-${vinJson.vin}`;
  const img = document.createElement('img');
  img.setAttribute('id', imgId);
  img.setAttribute('src', vinJson.photo_url);
  img.setAttribute('alt', vinJson.vin);

  // Set the photo size to a fixed size, because each photo has different size
  img.style.height = '100px';
  img.style.width = '200px';

  photoCell.appendChild(img);  
}

function addVin(vinJson) {
  if (cachedVins.has(vinJson.vin)) {
    return;
  }

  addVinToTable(vinJson);
  cachedVins.set(vinJson.vin, vinJson);
}

form.addEventListener('submit', (event) => {
  // By default when submitting a 'form',
  // the browser tries to submit the data to somewhere
  event.preventDefault();

  const formData = new FormData(form);
  const vinNumber = formData.get('vin').trim();

  if (cachedVins.has(vinNumber)) {
    return;
  }

  lookupVin(vinNumber)
    .then(addVin)
    .catch(error => alert(error));
});

// List all VINs during initialization
listVins()
  .then(vinsJson => {
    for (const vinJson of vinsJson.vins) {
      addVin(vinJson);
    }
  })
  .catch(error => alert(`Failed to fetch VINs: ${error}.`));
