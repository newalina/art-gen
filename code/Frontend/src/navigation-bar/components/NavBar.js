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
            <p>
              <b>Melting. Rising. Displacing. </b>
            </p>
            <p>
              <b>
                Each word understood as part of the implications of climate
                change, this story we know.
              </b>
            </p>
            <p>
              <b>
                It is also the story of worlds that become visibly entangled
                within the hypermedia of socio-environmental data.
              </b>
            </p>
            <p>
              <b>
                REGENERATIVE is an experimental exploration of ways to visualise
                the innate interconnected nature of worlds damaged by human
                interactions.
              </b>
            </p>
            <p>
              <b>
                Our project mediates digital art as alternative realities and
                evidence of damage.
              </b>
            </p>
            <p>
              <b>
                Truths and tensions are formed through the dialogue between
                users and their creations.
              </b>
            </p>
            <p>
              <b>The extent of what you create is beyond our understanding.</b>
            </p>
            <p>
              Thanks to Alexander Pratt (backend lead | project architecture),
              Alina Kim (team lead | project design and direction), David Doan
              (data processing), Haiyang Wang (research and development), Gus
              LeTourneau (profile page and media), Malique Bodie (database
              management), Morgann Thain (research and development), Yingjia Liu
              (controls page and routing) for making this project possible.
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
