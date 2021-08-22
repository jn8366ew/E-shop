// Authentication

export const SIGNUP_SUCCESS = 'SIGNUP_SUCCESS';
export const SIGNUP_FAIL = 'SIGNUP_FAIL';
export const LOGIN_SUCCESS = 'LOGIN_SUCCESS';
export const LOGIN_FAIL = 'LOGIN_FAIL';
export const AUTHENTICATED_SUCCESS = 'AUTHENTICATED_SUCCESS';
export const AUTHENTICATED_FAIL = 'AUTHENTICATED_FAIL';
export const REFRESH_SUCCESS = 'REFRESH_SUCCESS';
export const REFRESH_FAIL = 'REFRESH_FAIL';
export const SET_AUTH_LOADING = 'SET_AUTH_LOADING';
export const REMOVE_AUTH_LOADING = 'REMOVE_AUTH_LOADING';
export const ACTIVATION_SUCCESS = 'ACTIVATION_SUCCESS';
export const ACTIVATION_FAIL = 'ACTIVATION_FAIL';
export const USER_LOADED_SUCCESS = 'USER_LOADED_SUCCESS';
export const USER_LOADED_FAIL = 'USER_LOADED_FAIL';
export const LOGOUT = 'LOGOUT';
export const RESET_PASSWORD_SUCCESS = 'RESET_PASSWORD_SUCCESS';
export const RESET_PASSWORD_FAIL = 'RESET_PASSWORD_FAIL';
export const RESET_PASSWORD_CONFIRM_SUCCESS = 'RESET_PASSWORD_CONFIRM_SUCCESS';
export const RESET_PASSWORD_CONFIRM_FAIL = 'RESET_PASSWORD_CONFIRM_FAIL';
export const GOOGLE_AUTH_SUCCESS = 'GOOGLE_AUTH_SUCCESS';
export const GOOGLE_AUTH_FAIL = 'GOOGLE_AUTH_FAIL';
export const FACEBOOK_AUTH_SUCCESS = 'FACEBOOK_AUTH_SUCCESS';
export const FACEBOOK_AUTH_FAIL = 'FACEBOOK_AUTH_FAIL';

// Categories
export const GET_CATEGORIES_SUCCESS = 'GET_CATEGORIES_SUCCESS';
export const GET_CATEGORIES_FAIL = 'GET_CATEGORIES_FAIL';

// Product

export const GET_PRODUCT_SUCCESS = 'GET_PRODUCT_SUCCESS';
export const GET_PRODUCT_FAIL = 'GET_PRODUCT_FAIL';
export const GET_PRODUCTS_SUCCESS = 'GET_PRODUCTS_SUCCESS';
export const GET_PRODUCTS_FAIL = 'GET_PRODUCTS_FAIL';
export const GET_PRODUCTS_BY_ARRIVAL_SUCCESS = 'GET_PRODUCTS_BY_ARRIVAL_SUCCESS';
export const GET_PRODUCTS_BY_ARRIVAL_FAIL = 'GET_PRODUCTS_BY_ARRIVAL_FAIL';
export const GET_PRODUCTS_BY_SOLD_SUCCESS = 'GET_PRODUCTS_BY_SOLD_SUCCESS';
export const GET_PRODUCTS_BY_SOLD_FAIL = 'GET_PRODUCTS_BY_SOLD_FAIL';
export const SEARCH_PRODUCTS_SUCCESS = 'SEARCH_PRODUCTS_SUCCESS';
export const SEARCH_PRODUCTS_FAIL = 'SEARCH_PRODUCTS_FAIL';
export const RELATED_PRODUCTS_SUCCESS = 'RELATED_PRODUCTS_SUCCESS';
export const RELATED_PRODUCTS_FAIL = 'RELATED_PRODUCTS_FAIL';
export const FILTER_PRODUCTS_SUCCESS = 'FILTER_PRODUCTS_SUCCESS';
export const FILTER_PRODUCTS_FAIL = 'FILTER_PRODUCTS_FAIL';


// Local Cart without Async
export const ADD_ITEM = 'ADD_ITEM';
export const GET_TOTAL = 'GET_TOTAL';
export const GET_ITEM_TOTAL = 'GET_ITEM_TOTAL';
export const GET_ITEMS = 'GET_ITEMS';
export const UPDATE_ITEM = 'UPDATE_ITEM';
export const REMOVE_ITEM = 'REMOVE_ITEM';
export const EMPTY_ITEM = 'EMPTY_CART';


// Database Cart
export const ADD_ITEM_SUCCESS = 'ADD_ITEM_SUCCESS ';
export const ADD_ITEM_FAIL = 'ADD_ITEM_FAIL';
export const GET_TOTAL_SUCCESS = 'GET_TOTAL_SUCCESS';
export const GET_TOTAL_FAIL = 'GET_TOTAL_FAIL';
export const GET_ITEM_TOTAL_SUCCESS = 'GET_ITEM_TOTAL_SUCCESS';
export const GET_ITEM_TOTAL_FAIL = 'GET_ITEM_TOTAL_FAIL';
export const GET_ITEMS_SUCCESS = 'GET_ITEMS_SUCCESS';
export const GET_ITEMS_FAIL = 'GET_ITEMS_FAIL';
export const UPDATE_ITEM_SUCCESS = 'UPDATE_ITEM_SUCCESS';
export const UPDATE_ITEM_FAIL = 'UPDATE_ITEM_FAIL';
export const REMOVE_ITEM_SUCCESS = 'REMOVE_ITEM_SUCCESS';
export const REMOVE_ITEM_FAIL = 'REMOVE_ITEM_FAIL';
export const EMPTY_ITEM_SUCCESS = 'EMPTY_ITEM_SUCCESS';
export const EMPTY_ITEM_FAIL = 'EMPTY_ITEM_FAIL';
export const SYNCH_CART_SUCCESS = 'SYNCH_CART_SUCCESS';
export const SYNCH_CART_FAIL = 'SYNCH_CART_FAIL';


// Shipping
export const GET_SHIPPING_OPTIONS_SUCCESS = 'GET_SHIPPING_OPTIONS_SUCCESS';
export const GET_SHIPPING_OPTIONS_FAIL = 'GET_SHIPPING_OPTIONS_FAIL';


// Payment
export const GET_PAYMENT_TOTAL_SUCCESS = 'GET_PAYMENT_TOTAL_SUCCESS';
export const GET_PAYMENT_TOTAL_FAIL = 'GET_PAYMENT_TOTAL_FAIL';
export const LOAD_BT_TOKEN_SUCCESS = 'LOAD_BT_TOKEN_SUCCESS';
export const LOAD_BT_TOKEN_FAIL = 'LOAD_BT_TOKEN_FAIL';
export const PAYMENT_SUCCESS = 'PAYMENT_SUCCESS';
export const PAYMENT_FAIL = 'PAYMENT_FAIL';
export const RESET_PAYMENT_INFO = 'RESET_PAYMENT_INFO';
export const SET_PAYMENT_LOADING = 'SET_PAYMENT_LOADING'
export const REMOVE_PAYMENT_LOADING = 'REMOVE_PAYMENT_LOADING'

// Alerts
export const SET_ALERT = 'SET_ALERT';
export const REMOVE_ALERT = 'REMOVE_ALERT';


// Orders
export const GET_ORDERS_SUCCESS = 'GET_ORDERS_SUCCESS';
export const GET_ORDERS_FAIL = 'GET_ORDERS_FAIL';
export const GET_ORDER_DETAIL_SUCCESS = 'GET_ORDER_DETAIL_SUCCESS';
export const GET_ORDER_DETAIL_FAIL = 'GET_ORDER_DETAIL_FAIL';