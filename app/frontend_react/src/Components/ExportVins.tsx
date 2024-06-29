import { FormEvent } from "react";

export enum ExportFormat {
  CSV = 'csv',
  PARQUET = 'parquet',
};

export type ExportVinsArgs = {
  onExportClicked?: (arg: ExportFormat) => void;
};

export default function ExportVins({ onExportClicked }: ExportVinsArgs) {
  const exportFormatName = 'export-format'

  function submitForm(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (onExportClicked) {
      const formData = new FormData(event.target as HTMLFormElement);
      const exportFormat: string = formData.get(exportFormatName)!.toString();

      // Return a JSON object whose key is the string enum value
      // and the value is the string enum object
      const allExportFormats = Object.fromEntries(
        Object
          .values(ExportFormat)
          .map(expFormat => [expFormat.toString(), expFormat])
      );

      if (Object.keys(allExportFormats).includes(exportFormat)) {
        onExportClicked(allExportFormats[exportFormat])
      } else {
        throw new Error(`Invalid export format \"${exportFormat}\".`);
      }
    }
  }

  return (
    <>
      <form className="vin-lookup-form" onSubmit={submitForm}>
        <label>Select export format:</label>
        <select name={exportFormatName}>
          <option value={ExportFormat.CSV}>CSV</option>
          <option value={ExportFormat.PARQUET}>Parquet</option>
        </select>

        <br />

        <button className="button-primary" 
                type="submit"
                style={{ marginLeft: '5px'}}>
          Export
        </button>
      </form>
    </>
  );
}
