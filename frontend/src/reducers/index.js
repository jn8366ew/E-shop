import { combineReducers } from "redux";
import auth from './auth';
import alert from './alerts';
import categories from "./categories";
import products from "./products";
import cart from "./cart"
import shipping from "./shipping";
import payment from "./payment";
import orders from "./orders"
import profile from "./profile"
import coupons from "./coupons";
import reviews from "./reviews";

export default combineReducers({
    auth,
    alert,
    categories,
    payment,
    products,
    cart,
    shipping,
    orders,
    coupons,
    profile,
    reviews,
});

