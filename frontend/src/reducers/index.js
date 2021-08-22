import { combineReducers } from "redux";
import auth from './auth';
import alert from './alerts';
import categories from "./categories";
import products from "./products";
import cart from "./cart"
import shipping from "./shipping";
import payment from "./payment";
import orders from "./orders"

export default combineReducers({
    auth,
    alert,
    categories,
    payment,
    products,
    cart,
    shipping,
    orders,
});

