export default function SearchVin({ onSearchClicked }) {
  const searchName = 'search';
  function submitForm(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const lookupVin = formData.get('lookup-vin');
    onSearchClicked(lookupVin);
  }

  return (
    <>
      <form className="vin-lookup-form" onSubmit={submitForm}>
        <label>Lookup a VIN</label>
        <input className="u-full-width" type="search" name="lookup-vin" />
        <button className="button-primary" type="submit" name={searchName}>Search</button>
      </form>
    </>
  );
}
