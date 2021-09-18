import React, { Fragment, useState, useEffect } from 'react';
import { Redirect } from 'react-router-dom'
import { connect } from 'react-redux';
import { Helmet } from 'react-helmet';


import { get_products_by_arrival,
        get_products_by_sold
} from "../actions/products";
import {
    add_item,
    get_items,
    get_total,
    get_item_total
} from "../actions/cart";


import LandingPage from "../components/LandingPage";


const Home = ({
      products_arrival,
      products_sold,

      // actions from product
      get_products_by_arrival,
      get_products_by_sold,

      // actions from cart
      add_item,
      get_items,
      get_total,
      get_item_total

}) => {
    const [redirect, setRedirect] = useState(false);

    useEffect(() => {
        // scroll to the top of homepage
        window.scrollTo(0, 0);

        get_products_by_arrival();
        get_products_by_sold();
    }, []);

    if (redirect)
        return <Redirect to='/cart-or-continue-shopping' />;

    return (
        <Fragment>
            <Helmet>
                <meta charSet="utf-8" />
                <meta name="description" content="Home Helmet application" />
                <title>E-Shop | Home</title>
                {/* <link rel="canonical" href="http://mysite.com/example" /> */}
            </Helmet>
            <LandingPage
                // props of LandingPage
                products_arrival={products_arrival}
                products_sold={products_sold}
                add_item={add_item}
                get_items={get_items}
                get_total={get_total}
                get_item_total={get_item_total}
                setRedirect={setRedirect}
            />
        </Fragment>
    );
};


// 2개의 리덕스 state를 불러온다
const mapStateToProps = state => ({
    products_arrival: state.products.products_arrival,
    products_sold: state.products.products_sold
});

export default connect(mapStateToProps, {
    get_products_by_arrival,
    get_products_by_sold,
    add_item,
    get_items,
    get_total,
    get_item_total
})(Home);
