import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import UserIconPopup from '../../user-profile/component/UserIconPopup';
import styles from "./NavBar.module.css";
import HomeIcon from './HomeIcon';
import InfoIcon from './InfoIcon';


const Navbar = () => {

    const [isModalOpen, setIsModalOpen] = useState(false);

    const toggleModal = () => setIsModalOpen(!isModalOpen);

    return (
        <nav className={styles.navbar}>
            <Link to="/home">
            <div className={styles.homeIcon}>
                <HomeIcon />
            </div>
            </Link>

            <div className={styles.infoIcon}>
                <InfoIcon onClick={toggleModal}/> 
            </div>               

            {isModalOpen && (
                <div className={styles.modal}>
                    <div className={styles.modalContent}>
                        <span className={styles.closeButton} onClick={toggleModal}>&times;</span>
                        <p>Here is some information about the website...</p>
                        <p>Here is some information about the website...</p>
                        <p>Here is some information about the website...</p>
                        <p>Here is some information about the website...</p>
                        <p>Here is some information about the website...</p>
                        <p>Here is some information about the website...</p>
                        <p>Here is some information about the website...</p>
                        <p>Here is some information about the website...</p>
                    </div>
                </div>
            )}        

            <UserIconPopup />
            
        </nav>
    );
};

export default Navbar;
