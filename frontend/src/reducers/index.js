import { combineReducers } from "redux";
import auth from './auth';
import alert from './alerts';
import categories from "./categories";
import products from "./products";
import cart from "./cart"
import shipping from "./shipping";

export default combineReducers({
    auth,
    alert,
    categories,
    products,
    cart,
    shipping,
});

