"use client"
import Image from "next/image";
import styles from "./page.module.css";
import { useState, useEffect } from "react";
// import { fetchImage } from "./controllers/data";

interface NasaApiResponse {
  url: string;
  hdurl: string;
  title: string;
  explanation: string;
}

export default function Home() {
  const [data, setData] = useState<NasaApiResponse | null>(null);
  const [isLoading, setLoading] = useState(true);

  // useEffect(() => {
  //   fetchImage
  //     .then((res) => res.json())
  //     .then((data) => {
  //       setData(data);
  //       setLoading(false);
  //     });
  // }, []);

  // async function getImage(username: string) {
  //   const res = await fetch(`https://api.example.com/image/${username}`);
  //   return res.json();
  // }
  const fetchImage = async () => {
    // Replace the api key with your own
    const apiUrl = "https://api.nasa.gov/planetary/apod?api_key=REPLACE_THIS_WITH_YOUR_API_KEY";
    try {
      const res = await fetch(apiUrl);
      const data = await res.json();
      setData(data);
    } catch (error) {
      console.error("Error fetching data from NASA API:", error);
    } finally {
      setLoading(false);
    }
      
  };

  // useEffect (() => {
  //   fetchImage();
  // }, []);

  // if (isLoading) return <p>Loading...</p>;
  // if (!data) return <p>No profile data</p>;

  return (
    <main className={styles.main}>
      <div className={styles.description}>
        <p>
          Get started by editing&nbsp;
          <code className={styles.code}>app/page.tsx</code>
        </p>

        {/* The fetch data button */}
        <div>
          <button onClick={fetchImage}> 
            Fetch data
          </button>
          <h1>{data?.title}</h1>
          {!isLoading && data && <img src={data.url} alt={data.title} />}
          {isLoading && <p>Loading...</p>}

          {/* display the explaination of the image if we have the data */}
          {data? <p>{data.explanation}</p> : <p>No profile data</p>}
        </div>

        <div>
          <a
            href="https://vercel.com?utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
            target="_blank"
            rel="noopener noreferrer"
          >
            By{" "}
            <Image
              src="/vercel.svg"
              alt="Vercel Logo"
              className={styles.vercelLogo}
              width={100}
              height={24}
              priority
            />
          </a>
        </div>
      </div>

      <div className={styles.center}>
        <Image
          className={styles.logo}
          src="/next.svg"
          alt="Next.js Logo"
          width={180}
          height={37}
          priority
        />
      </div>

      <div className={styles.grid}>
        <a
          href="https://nextjs.org/docs?utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
          className={styles.card}
          target="_blank"
          rel="noopener noreferrer"
        >
          <h2>
            Docs <span>-&gt;</span>
          </h2>
          <p>Find in-depth information about Next.js features and API.</p>
        </a>

        <a
          href="https://nextjs.org/learn?utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
          className={styles.card}
          target="_blank"
          rel="noopener noreferrer"
        >
          <h2>
            Learn <span>-&gt;</span>
          </h2>
          <p>Learn about Next.js in an interactive course with&nbsp;quizzes!</p>
        </a>

        <a
          href="https://vercel.com/templates?framework=next.js&utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
          className={styles.card}
          target="_blank"
          rel="noopener noreferrer"
        >
          <h2>
            Templates <span>-&gt;</span>
          </h2>
          <p>Explore starter templates for Next.js.</p>
        </a>

        <a
          href="https://vercel.com/new?utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
          className={styles.card}
          target="_blank"
          rel="noopener noreferrer"
        >
          <h2>
            Deploy <span>-&gt;</span>
          </h2>
          <p>
            Instantly deploy your Next.js site to a shareable URL with Vercel.
          </p>
        </a>
      </div>
    </main>
  );
}
