import {
    GET_CATEGORIES_FAIL,
    GET_CATEGORIES_SUCCESS
} from "../actions/types";

const initialState = {
    categories: null
};

export default function(state = initialState, action) {
    const { type, payload } = action;

    // action/categories.js 와 연동
    switch (type) {
        case GET_CATEGORIES_SUCCESS:
            return {
                ...state,
                categories: payload.categories
            }

        case GET_CATEGORIES_FAIL:
            return {
                ...state,
                categories: null
            }

        default:
            return state
    }
}