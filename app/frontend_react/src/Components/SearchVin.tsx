import { FormEvent } from "react";

export type SearchVinArgs = {
  onSearchClicked?: (arg: string) => void;
};

export default function SearchVin({ onSearchClicked }: SearchVinArgs) {
  const searchName = 'lookup-vin';

  function submitForm(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (onSearchClicked) {
      const formData = new FormData(event.target as HTMLFormElement);
      const lookupVin = formData.get(searchName)!.toString();
      onSearchClicked(lookupVin);
    }
  }

  return (
    <>
      <form className="vin-lookup-form" onSubmit={submitForm}>
        <label>Lookup a VIN</label>
        <input className="u-full-width" type="search" name={searchName} />
        <button className="button-primary" type="submit">Search</button>
      </form>
    </>
  );
}
