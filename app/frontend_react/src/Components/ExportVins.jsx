export default function ExportVins({ onExportClicked }) {
  const exportFormatName = 'export-format'

  function submitForm(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const exportFormat = formData.get(exportFormatName);
    onExportClicked(exportFormat);
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
