import { FormEvent } from "react";

export type ExportVinsArgs = {
  onExportClicked?: (arg: string) => void;
};

export default function ExportVins({ onExportClicked }: ExportVinsArgs) {
  const exportFormatName = 'export-format'

  function submitForm(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (onExportClicked) {
      const formData = new FormData(event.target as HTMLFormElement);
      const exportFormat = formData.get(exportFormatName)!.toString()
      onExportClicked(exportFormat);
    }
  }

  return (
    <>
      <form className="vin-lookup-form" onSubmit={submitForm}>
        <label>Select export format:</label>
        <select name={exportFormatName}>
          <option value="csv">CSV</option>
          <option value="parquet">Parquet</option>
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
