import React, { Fragment, useState, useEffect } from 'react';
import { connect } from 'react-redux';
import {
    get_items,
    get_total,
    get_item_total
} from "../actions/cart";
import { list_orders } from "../actions/orders";


const DashBoard = ({
   get_items,
   get_total,
   get_item_total,
   list_orders,
   orders,
   user

}) => {
    const [display, setDisplay] = useState('user_info')


    useEffect(() => {
        get_items();
        get_total();
        get_item_total();
        list_orders();
    }, []);

    const userInfo = () => {
        return (
            <div className='card mb-5'>
                <h3 className='card-header'>User Information</h3>
                <ul className='list-group'>
                    <li className='list-group-item'>
                        <strong>First Name: </strong>
                        {
                            user &&
                            user !== null &&
                            user !== undefined ?
                            user.first_name : <Fragment></Fragment>
                        }
                    </li>
                    <li className='list-group-item'>
                        <strong>Last Name: </strong>
                        {
                            user &&
                            user !== null &&
                            user !== undefined ?
                                user.last_name : <Fragment></Fragment>
                        }
                    </li>
                    <li className='list-group-item'>
                        <strong>Email: </strong>
                        {
                            user &&
                            user !== null &&
                            user !== undefined ?
                                user.email : <Fragment></Fragment>
                        }
                    </li>
                </ul>
            </div>
        );
    };

    const purchase_history = () => {
        return (
            <div> purchase_history </div>
        )
    }



    const renderData = () => {
        if (display === 'user_info') {
            return (
                <Fragment>
                    {userInfo()}
                </Fragment>
            );
        } else if (display === 'purchase_history') {
            return (
                <Fragment>
                    {purchase_history()}
                </Fragment>
            );
        }
    };

    return (
        <div className='container mt-5'>
            <div className='row'>
                <div className='col-3'>
                    <div className='card'>
                        <h3 className='card-header'>
                            Dashboard Links
                        </h3>
                        <ul className='list-group'>
                            <li
                                className='list-group-item'
                                style={{ cursor: 'pointer' }}
                                onClick={() => setDisplay('user_info')}
                            >
                                {
                                    display === 'user_info' ? (
                                        <strong>User Info</strong>
                                    ) : (
                                        <Fragment>User Info</Fragment>
                                    )
                                }

                            </li>
                            <li
                                className='list-group-item'
                                style={{ cursor: 'pointer' }}
                                onClick={() => setDisplay('purchase_history')}
                            >
                                {
                                    display === 'purchase_history' ? (
                                        <strong>Purchase History</strong>
                                    ) : (
                                        <Fragment>Purchase History</Fragment>
                                    )
                                }

                            </li>
                        </ul>
                    </div>
                </div>
                <div className='col-9'>
                    {renderData()}
                </div>
            </div>
        </div>
    );

}

const mapStateToProps = state => ({
    orders: state.orders.orders,
    user: state.auth.user,

});

export default connect(mapStateToProps, {
    get_items,
    get_total,
    get_item_total,
    list_orders


})(DashBoard);