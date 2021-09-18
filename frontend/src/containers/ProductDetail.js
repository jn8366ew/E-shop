import React, { useState, useEffect } from 'react'
import {Redirect} from "react-router-dom";
import { Helmet } from 'react-helmet';

import { connect } from 'react-redux';
import {
    get_product,
    get_related_products
} from '../actions/products';
import {
    add_item,
    get_items,
    get_total,
    get_item_total
} from '../actions/cart'


import {
    get_reviews,
    get_review,
    create_review,
    update_review,
    delete_review,
    filter_review,
} from "../actions/reviews";

import Card from "../components/Card";
import ProductDetailCard from "../components/ProductDetailCard";
import LeaveReview from "../components/LeaveReview";
import Reviews from "../components/Reviews";
import Stars from "../components/Stars";

const ProductDetail = ({
    match,
    product,
    related_products,
    get_product,
    get_related_products,
    add_item,
    get_items,
    get_total,
    get_item_total,
    isAuthenticated,
    review,
    reviews,
    get_reviews,
    get_review,
    create_review,
    update_review,
    delete_review,
    filter_review,
}) => {
    const [loginRedirect, setLoginRedirect] = useState(false);
    const [redirect, setRedirect] = useState(false);

    const [formData, setFormData] = useState({
        comment: ''
    });

    const [rating, setRating] = useState(5.0)
    const { comment } = formData;


    //
    useEffect(() => {
        if (
            isAuthenticated !== null &&
            isAuthenticated !== undefined
        ) {
            if (
                isAuthenticated &&
                review &&
                review !== null &&
                review !== undefined &&
                review.comment &&
                review.comment !== null &&
                review.comment !== undefined
            ) {
               setFormData({
                   comment: review.comment
               });
            } else {
                setFormData({
                    comment: ''
                })
            }
        }
        // when review updates, isAuthenticated also updates.
    }, [review, isAuthenticated]);




    useEffect(() => {
        window.scrollTo(0, 0);
        const productId = match.params.id;
        get_product(productId);
        get_related_products(productId);

        // use match.params.id to restart action creators
        // by changing product_id in url.
    }, [match.params.id]);



    // useEffect for get_reviews
    useEffect(() => {
        const productId = match.params.id;
        get_reviews(productId);
    }, [match.params.id ]);


    // useEffect for get_review
    useEffect(() => {
        const productId = match.params.id;
        get_review(productId);
    }, [match.params.id, isAuthenticated]);


    const onChange = e => setFormData({...formData, [e.target.name]: e.target.value});

    const requireLogin = e => {
        e.preventDefault();

        setLoginRedirect(true);
    }

    // create review function
    const leaveReview = e => {
        e.preventDefault();

        const productId = match.params.id;

        if (rating !== null)
            create_review(productId, rating, comment)
    };

    const updateReview = e => {
        e.preventDefault();

        const productId = match.params.id;

        if (rating !== null)
            update_review(productId, rating, comment);
    };

    const deleteReview = () => {
        const productId = match.params.id;

        const fetchData = async () => {
            await delete_review(productId);
            await get_reviews(productId);
            setFormData({
                comment: ''
            });
        };

        fetchData();

    };

    const filterReviews = (numStars) => {
        const productId = match.params.id;

        filter_review(productId, numStars);

    };

    const getReviews = () => {
        const productId = match.params.id;

        get_reviews(productId)
    }


    const getRelatedProducts = () => {
        if (
            related_products &&
            related_products !== null &&
            related_products !== undefined &&
            related_products.length !== 0
        ) {
            return related_products.map((product, index) => (
                <div key={index} className='col-4'>
                    <Card
                        product={product}
                        add_item={add_item}
                        get_items={get_items}
                        get_total={get_total}
                        get_item_total={get_item_total}
                        setLoginRedirect={setLoginRedirect}
                        setRedirect={setRedirect}

                    />
                </div>
            ))
        }
    };

    const getLeaveReviewComponent = () => {
        if (isAuthenticated) {
            // For create a review
            if (
                review &&
                review !== null &&
                review !== undefined &&
                Object.keys(review).length === 0
            ) {
                return (
                    <LeaveReview
                        review={review}
                        rating={rating}
                        setRating={setRating}
                        onSubmit={leaveReview}
                        onChange={onChange}
                        comment={comment}
                    />
                );
            }
            // logic for update review
            else if (
                    review &&
                    review !== null &&
                    review !== undefined &&
                    Object.keys(review).length !== 0) {
                        return (
                            <LeaveReview
                                review={review}
                                rating={rating}
                                setRating={setRating}
                                onSubmit={updateReview}
                                onChange={onChange}
                                comment={comment}
                                deleteReview={deleteReview}
                            />
                        );
                    }
            } else {
                return (
                    <button
                        className='btn btn-info'
                        onClick={requireLogin}
                    >
                        Login to write a review
                    </button>
                );
            }
    };

    if (loginRedirect)
        return <Redirect to='/login' />

    if (redirect)
        return <Redirect to='/cart-or-continue-shopping' />;

    return (
        <div className='container mt-5'>
            <Helmet>
                <meta charSet="utf-8" />
                <meta name="description" content="ProductDetail Helmet application" />
                <title>E-Shop | Product Detail {`${
                    product &&
                    product !== null &&
                    product !== undefined &&
                    product.name &&
                    product.name !== null &&
                    product.name !== undefined ? product.name : ''
                }`}</title>
                {/* <link rel="canonical" href="http://mysite.com/example" /> */}
            </Helmet>
            <ProductDetailCard
                product={product}
                add_item={add_item}
                get_items={get_items}
                get_total={get_total}
                get_item_total={get_item_total}
                setRedirect={setRedirect}
            />

            <hr />

            <section className='mt-5 mb-5'>
                <div className='row'>
                    <div className='col-3'>
                        <h2 className='mb-3'>Filter Reviews</h2>
                        <button
                            className='btn btn-primary btn-sm mb-3'
                            onClick={getReviews}
                        >
                            All
                        </button>
                        <div
                            className='mb-3'
                            style={{ cursor: 'pointer '}}
                            onClick={() => filterReviews(5)}
                        >
                            <Stars rating={5.0} />
                        </div>
                        <div
                            className='mb-3'
                            style={{ cursor: 'pointer '}}
                            onClick={() => filterReviews(4)}
                        >
                            <Stars rating={4.0} />
                        </div>
                        <div
                            className='mb-3'
                            style={{ cursor: 'pointer '}}
                            onClick={() => filterReviews(3)}
                        >
                            <Stars rating={3.0} />
                        </div>
                        <div
                            className='mb-3'
                            style={{ cursor: 'pointer '}}
                            onClick={() => filterReviews(2)}
                        >
                            <Stars rating={2.0} />
                        </div>
                        <div
                            className='mb-3'
                            style={{ cursor: 'pointer '}}
                            onClick={() => filterReviews(1)}
                        >
                            <Stars rating={1.0} />
                        </div>


                        <h2>Write a Review</h2>
                        <p className='mb-3'>
                            Your review is a great help for customers and seller
                        </p>
                        {getLeaveReviewComponent()}
                    </div>
                    <div className='col-7 offset-2'>
                        <h2 className='mb-5'>Customer Reviews</h2>
                        <Reviews reviews={reviews} />
                    </div>
                </div>

            </section>

            <section className='mt-5'>
                <h2 className='mt-5'>Related Products:</h2>
                <div className='row mt-5 ml-5 mr-5'>
                    {getRelatedProducts()}
                </div>
            </section>



        </div>
    )
};






const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated,
    product: state.products.product,
    related_products: state.products.related_products,
    review: state.reviews.review,
    reviews: state.reviews.reviews

});

export default connect(mapStateToProps, {
    get_product,
    get_related_products,
    add_item,
    get_items,
    get_total,
    get_item_total,
    get_reviews,
    get_review,
    create_review,
    update_review,
    delete_review,
    filter_review,

})(ProductDetail);