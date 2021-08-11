import React from "react";
import { connect } from 'react-redux';
import CartItem from "../components/CartItem";
import {setAlert} from "../actions/alert";



const Checkout = ({
    items,
    total_items
}) => {
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
    return (
        <div className='container mt-5 mb-5'>
            <div className='row'>
                <div className='col-7'>
                    {showItems()}
                </div>
                <div className='col-5'>

                </div>
            </div>
        </div>
    )
};

const mapStateToProps = state => ({
   items: state.cart.items,
   total_items: state.cart.total_items
});


export default connect(mapStateToProps, {})(Checkout);