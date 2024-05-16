export default function ExportVins({ onExportClicked }) {

  function submitForm(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const exportFormat = formData.get('export-format');
    onExportClicked(exportFormat);
  }

  return (
    <>
      <form className="vin-lookup-form" onSubmit={submitForm}>
        <label>Select export format:</label>
        <select name="export-format">
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
