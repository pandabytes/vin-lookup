import { Vin } from '../types';

function VinRow({ vinNumber, make, model, modelYear, bodyClass, photoUrl }: Vin) {
  return (
    <tr>
      <td>{vinNumber}</td>
      <td>{make}</td>
      <td>{model}</td>
      <td>{modelYear}</td>
      <td>{bodyClass}</td>
      <td>
        <img id={`img-${vinNumber}`}
             src={photoUrl}
             alt={vinNumber}
             style={{ height: '100px', width: '200px' }} />
      </td>
    </tr>
  );
}

export default function VinsTable({ vins }: { vins: Array<Vin> }) {
  const vin_rows = vins.map(vin =>
    <VinRow key={vin.vinNumber}
            vinNumber={vin.vinNumber}
            make={vin.make}
            model={vin.model}
            modelYear={vin.modelYear}
            bodyClass={vin.bodyClass}
            photoUrl={vin.photoUrl} />
  );

  return (
    <table className="u-full-width vins-table">
      <thead>
        <tr>
          <th>VIN</th>
          <th>Make</th>
          <th>Model</th>
          <th>Year</th>
          <th>Body Class</th>
          <th>Photo</th>
        </tr>
      </thead>

      <tbody className="vins">
        {vin_rows}
      </tbody>
    </table>
  );
}
