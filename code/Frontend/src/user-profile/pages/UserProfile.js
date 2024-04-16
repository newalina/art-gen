import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './UserProfile.css'

const UserProfile = () => {
    const [isGrid, setIsGrid] = useState(true);

    const toggleView = () => {
        setIsGrid(!isGrid);
    };

    const responseFromApi = [
        ['https://randompicturegenerator.com/img/national-park-generator/g622bccfa3263195caf998e13ba1c1d43831b73fa15797fda0f7f3f325d267d6146ba55f8b845305057d3cb7594b74fb8_640.jpg'],
        ['https://randompicturegenerator.com/img/national-park-generator/g9380628fc6b35ab379a9ee67dc2a6c986577b4f52657c7a8fb819ce2b86b5400132340cd4ff951976827ea82bb301874_640.jpg'],
        ['https://randompicturegenerator.com/img/national-park-generator/g709061b49d4f0df7033480c9da3e3825b0ebdc7eeaa3a31901353e84e9b87685a3964173f199fdcadf818e45abe321b4_640.jpg'],
        ['https://randompicturegenerator.com/img/national-park-generator/gc28ded304cb3518636a01ecf8b7732c36a658da4cdd658065b70624a2abdf06f6f53071bd1abda95cc6f3d1b6d6dddb6_640.jpg'],
        ['https://randompicturegenerator.com/img/national-park-generator/g629fbb69eaefad4f698473fa2aa7e6c8c336e37cd3aa179058e56dbbc834157525d34901a9abb510e8976d00093c7716_640.jpg'],
        ['https://randompicturegenerator.com/img/national-park-generator/g223c48ee81956a261a48130a5a2193e80c04b86b9d15efd347aa73044b54ef298e73f54ec6e265e1840c380965ccbacf_640.jpg'],
        ['https://randompicturegenerator.com/img/national-park-generator/g351fda282375599c6fc8efc3e5e65666c8a686ad03ec367526e1d0c49a98d7dd0f756f675d7ef30950dc08300258afaf_640.jpg'],
        ['https://randompicturegenerator.com/img/national-park-generator/g43692b706a38b86e8b6b5cd160ebd0eed9748e541cceef5e3b042329d9ce9195bdec68fd936ccb1f9f6b2ad6afcba3e0_640.jpg'],
        ['https://randompicturegenerator.com/img/national-park-generator/ged4c9fb3943cde4e0320a442956fb6315073ae237eb38c0b651ed5e8915e80cae71d3e182deef7664da6666a4a4ba70f_640.jpg'],
        ['https://randompicturegenerator.com/img/national-park-generator/g910366c05c4459307f561917bf95c600007b71f03f97cdcac8f5599d9e128f754238f107e82df9e03cb531b6fb4d9197_640.jpg'],
        ['https://randompicturegenerator.com/img/national-park-generator/g18290695519504278647b9eb546cdeff0bd9ab0e26638bcd47fff20e657188abe9fab9a699780d4eddb8bf172f935f01_640.jpg'],
        ['https://randompicturegenerator.com/img/national-park-generator/ge5565564f564633d8cbc4d5c4e8a264e1da7802931b76bdca2428c73c26bc0db8d3431b4aa3a2c722f51f17842cdbf6e_640.jpg'],
        ['https://randompicturegenerator.com/img/national-park-generator/ge88b42ceccc0cdada9a466eacf8019a7e153b7f728003ff8601627293c0aacd7135f969723a2f3d5fd3939c296dee4e5_640.jpg'],
        ['https://randompicturegenerator.com/img/national-park-generator/gc97f498386cd4fc54d9723ed4f331e24fe69ba16cc2d487b7283bf6f75a87bf264c412d3f782876aa648caf0af82c9ab_640.jpg'],
        ['https://randompicturegenerator.com/img/national-park-generator/g91f71ae2b2afa710f67b3d61641ba37ef56f83e5542f7bf47852c3b1b20ed6a868e9436be59f57776065d4ab5349c06c_640.jpg'],
        ['https://randompicturegenerator.com/img/national-park-generator/ge4290ee08d35a651b01287320254787c28f0925b038712835227bec4a7be747aa3841fbf31e02123084616a2a5cb2791_640.jpg'],
        ['https://randompicturegenerator.com/img/national-park-generator/g0006086023a5ee189596aaafa505a5a598f0405db4b879bf59c515b9da783351111d35ee716fb286df19d0e3191256c2_640.jpg'],
        ['https://randompicturegenerator.com/img/national-park-generator/g7cab038303cf39a1fe3274ed0a4dc6069803514b4edb87218e5e39bc433d314006cc4c6d7c9f7489dea15c1d54316f47_640.jpg'],

    ];


    return (
        <div className={'container'}>
            <div className={'username-container'}>
                User Name
            </div>
            <div className={'view-toggle'} onClick={toggleView}>
                {isGrid ?
                    (<svg width="35" height="27" viewBox="0 0 35 27" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <rect x="0.516113" y="4.35498" width="6.09677" height="18.2903" fill="#D9D9D9"/>
                        <rect x="10.0967" width="14.8065" height="27" fill="#D9D9D9"/>
                        <rect x="28.387" y="4.35498" width="6.09677" height="18.2903" fill="#D9D9D9"/>
                    </svg>)
                    : (<svg width="35" height="35" viewBox="0 0 35 35" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <rect width="13.61" height="13.61" transform="matrix(-1 0 0 1 31.0005 0)" fill="#D9D9D9"/>
                        <rect width="13.61" height="13.61" transform="matrix(-1 0 0 1 13.6099 0)" fill="#D9D9D9"/>
                        <rect width="13.61" height="13.61" transform="matrix(-1 0 0 1 31.0002 17.3892)" fill="#D9D9D9"/>
                        <rect width="13.61" height="13.61" transform="matrix(-1 0 0 1 13.6099 17.3892)" fill="#D9D9D9"/>
                    </svg>)}
            </div>
            {isGrid ?
                (<div className="container">
                    <div id="image-grid" className={`grid-container grid`}>
                        {/* Images will be dynamically added here */}
                        {responseFromApi.map((image, index) => (
                            <div key={index} className="grid-item">
                                <img className="grid-item-img "src={image[0]} alt={`Image ${index}`} />
                            </div>
                        ))}
                    </div>
                </div>) :
                <div className="slider">
                    <div id="px-8 slides" className="slide-track">
                        {/* Map through responseFromApi and create divs for each image */}
                        {responseFromApi.map((imageUrl, index) => (
                            <div key={index} className="px-8 slide text-center">
                                <img className="grid-item-img" src={imageUrl[0]} alt={`Image ${index}`} />
                                {/* You can add additional content here if needed */}
                            </div>
                        ))}
                    </div>
                </div>}

            <div className="ok">
                <button className={'sign-out-button'} onClick={toggleView}>Sign Out</button>
            </div>
        </div>
    );
}

export default UserProfile;