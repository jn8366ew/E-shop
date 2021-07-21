import { combineReducers } from "redux";
import auth from './auth';
import alert from './alerts';


export default combineReducers({
    auth,
    alert
});

