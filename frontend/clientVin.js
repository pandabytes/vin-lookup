const form = document.querySelector("form"); // "form" is tagname
const loadingElement = document.querySelector(".loading"); // ".loading" is class
const API_URL = "http://localhost:8000";

const cachedVins = new Map()

async function lookupVin(vin) {
  const response = await fetch(`${API_URL}/lookup/${vin}`, { method: "GET", "content-type": "application/json" });
  if (!response.ok) {
    throw new Error(`VIN lookup api returned with a ${response.statusText}.`);
  }
  const vinJson = await response.json();
  return vinJson;
}

function addVin(vinJson) {
  const table = document.querySelector(".vins");
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
  modelYearCell.innerHTML = vinJson.modelYear;
  bodyClassCell.innerHTML = vinJson.bodyClass;

  const imgId = `img-${vinJson.vin}`;
  const img = document.createElement("img");
  img.setAttribute("id", imgId);
  img.setAttribute("src", vinJson.photoUrl);
  img.setAttribute("alt", vinJson.vin);

  // Set the photo size to a fixed size, because each photo has different size
  img.style.height = '100px';
  img.style.width = '200px';

  photoCell.appendChild(img);  
}

form.addEventListener("submit", (event) => {
  // By default when submitting a "form",
  // the browser tries to submit the data to somewhere
  event.preventDefault();

  const formData = new FormData(form);
  const vinNumber = formData.get("vin");
  console.log('vin number is', vinNumber);
  lookupVin(vinNumber)
    .then(vinJson => {
      console.log(vinJson);
      if (!cachedVins.has(vinJson.vin)) {
        addVin(vinJson);
      }
      cachedVins.set(vinJson.vin, vinJson);
    })
    .catch(error => console.log(error));
});
