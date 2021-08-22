import axios from 'axios'
import {
    GET_ORDERS_SUCCESS,
    GET_ORDERS_FAIL,
    GET_ORDER_DETAIL_SUCCESS,
    GET_ORDER_DETAIL_FAIL
} from './types'

export const list_orders = () => async dispatch => {
    if (localStorage.getItem('access')) {
        const config = {
            headers: {
                'Accept': 'application/json',
                'Authorization': `JWT ${localStorage.getItem('access')}`
            }
        };

        try {
            const res = await axios.get(`${process.env.REACT_APP_API_URL}/api/orders/get-orders`, config);

            // status 200일 시 result 리스트에 담긴 item 데이터를 받는다.
            if (res.status === 200) {
                dispatch({
                    type: GET_ORDERS_SUCCESS,
                    payload: res.data
                });
            } else {
                dispatch({
                    type: GET_ORDERS_FAIL
                });
            }

        } catch(err) {
            dispatch({
                type: GET_ORDERS_FAIL
            });
        }
    }
};

export const get_order_detail = transactionId => async dispatch => {
    if (localStorage.getItem('access')) {
        const config = {
            headers: {
                'Accept': 'application/json',
                'Authorization': `JWT ${localStorage.getItem('access')}`
            }
        };

        try {
            const res = await axios.get(`${process.env.REACT_APP_API_URL}/api/orders/get-order/${transactionId}`, config);

            // status 200일 시 result 리스트에 담긴 item 데이터를 받는다.
            if (res.status === 200) {
                dispatch({
                    type: GET_ORDER_DETAIL_SUCCESS,
                    payload: res.data
                });
            } else {
                dispatch({
                    type: GET_ORDER_DETAIL_FAIL
                });
            }

        } catch(err) {
            dispatch({
                type: GET_ORDER_DETAIL_FAIL
            });
        }
    }
}