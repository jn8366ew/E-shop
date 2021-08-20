import React, { useState, useEffect, Fragment } from "react";
import { Redirect } from 'react-router-dom';
import { connect } from 'react-redux';
import { refresh } from '../actions/auth'
import CartItem from "../components/CartItem";
import { get_shipping_options } from "../actions/shipping"
import {
    get_payment_total,
    get_client_token,
    process_payment
} from '../actions/payment';



const Checkout = ({
    items,
    total_items,
    refresh,
    get_shipping_options,
    shipping,
    get_payment_total,
    get_client_token,
    process_payment,
    isAuthenticated,
    user,
    clientToken,
    made_payment,
    loading,
    original_price,
    total_amount,
    total_compare_amount,
    estimated_tax,
    shipping_cost,
}) => {
    const [formData, setFormData] = useState({
        shipping_id: 0,
    });

    const {shipping_id} = formData;
    const onChange = e => setFormData({...formData, [e.target.name]: e.target.value});
    const onSubmit = e => {
        e.prevenDefault();
    };


    useEffect(() => {
        window.scrollTo(0, 0);


        // 새로운 엑세스 토큰을 받는다.
        refresh();
        get_shipping_options();
    }, []);

    useEffect(() => {
        get_client_token();
    }, [user]);

    useEffect(() => {
        get_payment_total(shipping_id);
    }, [shipping_id]);


    const showItems = () => {
        return (
            <div>
                <h4 className='text-muted mt-3'>
                    Your cart has {total_items} item(s)
                </h4>
                <hr/>
                {
                    items &&
                    items !== null &&
                    items !== undefined &&
                    items.length !== 0 &&
                    items.map((item, index) => {
                        let count = item.count;
                        return (
                            <div key={index}>
                                <CartItem
                                    item={item}
                                    count={count}
                                />
                            </div>
                        );
                    })
                }

            </div>
        );
    };

    const renderShipping = () => {
        if (shipping &&
            shipping !== null &&
            shipping !== undefined) {
            return (
                <div className='mb-5'>
                    {
                        shipping.map((shipping_option, index) => (
                            <div key={index} className='form-check'>
                                <input
                                    className='form-check-input'
                                    onClick={e => onChange(e)}
                                    value={shipping_option.id}
                                    name='shipping_id'
                                    type='radio'
                                    required
                                />
                                <label className='form-check-label'>
                                    {shipping_option.name} -
                                    ${shipping_option.price} ({shipping_option.time_to_delivery})
                                </label>
                            </div>
                        ))
                    }
                </div>
            );
        }
    };

    // 총 금액을 보여주는 화면
    const displayTotal = () => {
        let result = [];

        result.push(
            <Fragment>
                <span className='text-muted mr-3'>Items:</span>
                <span
                    className='mr-3 text-musted'
                    style={{
                        textDecoration: 'line-through'
                    }}
                >
                    ${total_compare_amount}
                </span>
            </Fragment>
        );

        result.push(
            <Fragment>
                <span className='text-muted mr-3'>Items:</span>
                <span
                    style={{
                        color: '#b12704'
                    }}
                >
                    ${original_price}
                </span>
            </Fragment>
        );

        // 배송
        if (shipping && shipping_id !== 0) {
            result.push(
                <div className='mt-3'>
                    <span className='text-muted mr-3'>
                        Shipping &amp; Handling:
                    </span>
                    <span style={{ color: '#b12704'}}>
                        ${shipping_cost}
                    </span>
                </div>
            );
        } else {
            result.push(
                <div className='mt-3'>
                    <span className='text-muted mr-3'>
                        Shipping &amp; Handling:
                    </span>
                    <span style={{ color: '#b12704'}}>
                        (Select shipping option)
                    </span>
                </div>
            );
        }

        //Display estimated tax
        result.push(
            <div className='mt-3'>
                <span className='text-muted mr-3'>
                    Estimated HST:
                </span>
                <span style={{ color: '#b12704'}}>
                    ${estimated_tax}
                </span>

            </div>
        );


        result.push(
            <div className='mt-3' style={{ color: '#b12704' }}>
                <span className='text-muted mr-3'>
                    Order Total:
                </span>
                <span>${total_amount}</span>
            </div>
        )


        return result;
    };



    if (made_payment) {
        return (<Redirect to='/thankyou'/>);
    };



    return (
        <div className='container mt-5 mb-5'>
            <div className='row'>
                <div className='col-7'>
                    {showItems()}
                </div>
                <div className='col-5'>
                    <h2 className='mb-3'>Order Summary</h2>
                    <div style={{ fontSize: '18px' }}>
                        {displayTotal()}
                        <form className='mt-5' Onsubmit={e => onSubmit(e)}>
                            <h4 className='text-muted mb-3'>
                                Select Shipping Option:
                            </h4>
                        {renderShipping()}
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
};

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated,
    user: state.auth.user,
    items: state.cart.items,
    total_items: state.cart.total_items,
    shipping: state.shipping.shipping,
    estimated_tax: state.payment.estimated_tax,
    clientToken: state.payment.clientToken,
    made_payment: state.payment.made_payment,
    loading: state.payment.loading,
    original_price: state.payment.original_price,
    total_amount: state.payment.total_amount,
    total_compare_amount: state.payment.total_compare_amount,
    shipping_cost: state.payment.shipping_cost
});


export default connect(mapStateToProps, {
    refresh,
    get_shipping_options,
    get_payment_total,
    get_client_token,
    process_payment
})(Checkout);