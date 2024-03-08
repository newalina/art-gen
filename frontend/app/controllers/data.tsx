/**
 * data.ts should contain all the functions used to fetch data from
 * the backend. This file should be imported in components. Components
 * should not contain any logic to fetch data.
 */

// import { assert } from "console";

const baseURL = `https://api.example.com/image/`;
let requestHeaders = new Headers();
requestHeaders.append("Content-Type", "application/json");

/**
 * Fetches the details of a product given its id.
 * @param ids: product ids
 * @returns { [] }: The details of the products
 */
export async function fetchImage() {
  const endpoint = "image";
  const requestOptions: RequestInit = {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  };

  try {
    const response = await fetch(baseURL + endpoint, requestOptions);
    if (!response.ok) {
      throw new Error("Network response was not OK");
    } else {
      const image: [] = await response.json();
      return image;
    }
  } catch (error) {
    console.error("Error fetching image:", error);
    throw error;
  }
}
