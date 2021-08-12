import React, { useState, useEffect } from "react";
import { connect } from 'react-redux';
import { refresh } from '../actions/auth'
import CartItem from "../components/CartItem";
import { get_shipping_options } from "../actions/shipping"



const Checkout = ({
    items,
    total_items,
    refresh,
    get_shipping_options,
    shipping,
}) => {
    const [formData, setFormData] = useState({
       shipping_id: 0,
    });

    const { shipping_id } = formData;
    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });
    const onSubmit = e => {
        e.prevenDefault();
    };


    useEffect(() => {
        window.scrollTo(0,0);


        // 새로운 엑세스 토큰을 받는다.
        refresh();
        get_shipping_options();
    }, []);
    const showItems = () => {
        return (
            <div>
                <h4 className='text-muted mt-3'>
                    Your cart has {total_items} item(s)
                </h4>
                <hr />
                {
                    items &&
                    items !== null &&
                    items !== undefined &&
                    items.length !== 0 &&
                    items.map((item, index) => {
                        let count = item.count;
                        return(
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
            return(
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
                                    {shipping_option.name} - ${shipping_option.price} ({shipping_option.time_to_delivery})
                                </label>
                            </div>
                        ))
                    }
                </div>
            )
        }
    };


    return (
        <div className='container mt-5 mb-5'>
            <div className='row'>
                <div className='col-7'>
                    {showItems()}
                </div>
                <div className='col-5'>
                    <h2 className='mb-3'>Order Summary</h2>
                    <p>ORDER DETAILS</p>
                    <form className='mt-5' Onsubmit={e => onSubmit(e)}>
                        <h4 className='text-muted mb-3'>
                            Select Shipping Option:
                        </h4>
                        {renderShipping()}

                    </form>
                </div>
            </div>
        </div>
    )
};

const mapStateToProps = state => ({
   items: state.cart.items,
   total_items: state.cart.total_items,
   shipping: state.shipping.shipping
});


export default connect(mapStateToProps, {
    refresh,
    get_shipping_options,
})(Checkout);