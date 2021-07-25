import { combineReducers } from "redux";
import auth from './auth';
import alert from './alerts';
import categories from "./categories";


export default combineReducers({
    auth,
    alert,
    categories,
});

