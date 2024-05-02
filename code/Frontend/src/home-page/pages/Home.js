import React from "react";
import { Link } from "react-router-dom";
import styles from "./Home.module.css";

const Home = () => {
  return (
    <div className={styles.container}>
      <h1 className={styles.title}>REGENERATIVE</h1>
      {/* <h1 className={styles.shadow}>REGENERATIVE</h1> */}
      <Link to="./controls" className={styles.buttonLink}>
        <button className={styles.button}>enter</button>
      </Link>
    </div>
  );
};

export default Home;
