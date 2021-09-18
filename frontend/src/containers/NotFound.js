import React from "react";
import { Link } from 'react-router-dom';
import { Helmet } from 'react-helmet';

import NotFoundImg from '../assets/NotFoundImg.jpg'

const notFound = () => (
    <div className='container mt-5 d-flex flex-column align-items-center'>
        <Helmet>
            <meta charSet="utf-8" />
            <meta name="description" content="Notfound Helmet application" />
            <title>E-Shop | 404 Not Found</title>
            {/* <link rel="canonical" href="http://mysite.com/example" /> */}
        </Helmet>
        <img className='w3-display-topmiddle w3-container'
             alt='404 Error Visual'
             src={NotFoundImg}
             style={{ height: '200px', width: '200px' }}/>
        <h1 className='display-3 mt-5'>404 Not Found</h1>

        <p className='text-muted'>
            The link you requested can't be found on our site.
        </p>
        <Link to='/' className='btn btn-success mt-5'>
            Back to Site
        </Link>
    </div>
);

export default notFound;