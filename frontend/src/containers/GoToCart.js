import React from 'react';
import { Helmet } from 'react-helmet';

import { Link } from 'react-router-dom'

const GoToCart = () => (
    <div className='container mt-5 d-flex flex-column justfiy-content-center align-items-center'>

        <Helmet>
            <meta charSet="utf-8" />
            <meta name="description" content="GoToCart Helmet application" />
            <title>E-Shop | GoToCart</title>
            {/* <link rel="canonical" href="http://mysite.com/example" /> */}
        </Helmet>
        <h2 className='text-muted mb-5'>
            Would you like to go to your cart or continue to checkout?
        </h2>
        <div className='card'>
            <div className='card-body'>
                <Link className='btn btn-warning' to='/cart'>
                    Go to Cart
                </Link>
                <span className='text-muted ml-3 mr-3'>or</span>
                <Link className='btn btn-primary' to='/checkout'>
                    Proceed to Checkout
                </Link>
            </div>
        </div>

    </div>
);

export default GoToCart;