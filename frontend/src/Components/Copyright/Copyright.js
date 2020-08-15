import React from 'react';
import './Copyright.css';

const Copyright = () => {
    return (
        <div className="copyright">
            <p className="content"> &copy;MBOA Services {new Date().getFullYear()} .All Rights Reserved. </p>
        </div>
    )
}

export default Copyright;