import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import UserIconPopup from "../../user-profile/component/UserIconPopup";
import styles from "./NavBar.module.css";
import HomeIcon from "./HomeIcon";
import InfoIcon from "./InfoIcon";

const Navbar = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const toggleModal = () => setIsModalOpen(!isModalOpen);

  const location = useLocation();
  const isHome = location.pathname === "/home";

  if (isHome) {
    return null;
  }

  return (
    <nav className={styles.navbar}>
      <Link to="/home">
        <div className={styles.homeIcon}>
          <HomeIcon />
        </div>
      </Link>

      <div className={styles.infoIcon}>
        <InfoIcon onClick={toggleModal} />
      </div>

      {isModalOpen && (
        <div className={styles.modal}>
          <div className={styles.modalContent}>
            <span className={styles.closeButton} onClick={toggleModal}>
              &times;
            </span>
            <p>Melting. Rising. Displacing. </p>
            <p>
              Each word understood as part of the implications of climate
              change, this story we know.
            </p>
            <p>
              It is also the story of worlds that become visibly entangled
              within the hypermedia of socio-environmental data.
            </p>
            <p>
              REGENERATIVE is an experimental exploration of ways to visualise
              the innate interconnected nature of worlds damaged by human
              interactions.
            </p>
            Our project mediates digital art as alternative realities and
            evidence of damage.
            <p>
              Truths and tensions are formed through the dialogue between users
              and their creations.
            </p>
            <p>The extent of what you create is beyond our understanding.</p>
            <p>
              Thanks to Alexander Pratt (<b>backend lead</b> | project
              architecture), Alina Kim (<b>team lead</b> | project design and
              direction), David Doan (data processing), Haiyang Wang (research
              and development), Gus LeTourneau (profile page and media), Malique
              Bodie (database management), Morgann Thain (research and
              development), Yingjia Liu (controls page and routing) for making
              this project possible.
            </p>
            <p>View our full documentation here.</p>
          </div>
        </div>
      )}

      <UserIconPopup />
    </nav>
  );
};

export default Navbar;
