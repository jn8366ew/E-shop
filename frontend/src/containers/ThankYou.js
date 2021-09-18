import React, { useEffect } from "react";
import { Link } from "react-router-dom";
import { Helmet } from 'react-helmet';
import { connect } from 'react-redux';
import { reset } from "../actions/payment";

const ThankYou = ({ reset }) => {

    useEffect(() => {
        reset();
        window.scrollTo(0, 0);
    }, []);

    return (
        <div className='container mt-5 d-flex flex-column align-items-center'>
            <Helmet>
                <meta charSet="utf-8" />
                <meta name="description" content="Thankyou page Helmet application" />
                <title>E-Shop | Thank you</title>
                {/* <link rel="canonical" href="http://mysite.com/example" /> */}
            </Helmet>
            <h1 className='display-2 mt-5'> Thank you </h1>
            <p className='text-muted'>
                Hope you enjoyed good time!
            </p>
            <Link to='/' className='btn btn-success mt-5'>
                Back to Site
            </Link>
        </div>
    );
}

export default connect(null, {reset})(ThankYou);