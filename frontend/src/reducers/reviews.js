import {
    GET_REVIEWS_SUCCESS,
    GET_REVIEWS_FAIL,
    GET_REVIEW_SUCCESS,
    GET_REVIEW_FAIL,
    CREATE_REVIEW_SUCCESS,
    CREATE_REVIEW_FAIL,
    UPDATE_REVIEW_SUCCESS,
    UPDATE_REVIEW_FAIL,
    DELETE_REVIEW_SUCCESS,
    DELETE_REVIEW_FAIL,
    FILTER_REVIEW_SUCCESS,
    FILTER_REVIEW_FAIL,
} from '../actions/types'


const initialState = {
    review: null,
    reviews: null
};


export default function(state = initialState, action) {
    const { type, payload } = action;

    switch(type) {
        case GET_REVIEWS_SUCCESS:
            return {
                ...state,
                reviews: payload.reviews
            }

        case GET_REVIEWS_FAIL:
            return {
                ...state,
                reviews: []
            }

        case GET_REVIEW_SUCCESS:
            return {
                ...state,
                review: payload.review
            }

        case GET_REVIEW_FAIL:
            return {
                ...state,
                review: {}
            }

        case CREATE_REVIEW_SUCCESS:
            return {
                ...state,
                review: payload.review,
                reviews: payload.reviews
            }

        case CREATE_REVIEW_FAIL:
            return {
                ...state,
                review: {},
                reviews: []
            }

        case UPDATE_REVIEW_SUCCESS:
            return {
                ...state,
                review: payload.review,
                reviews: payload.reviews
            }

        case UPDATE_REVIEW_FAIL:
            return {
                ...state
            }

        case DELETE_REVIEW_SUCCESS:
            return {
                ...state,
                review: {},
                reviews: []

            }

        case DELETE_REVIEW_FAIL:
            return {
                ...state
            }

        case FILTER_REVIEW_SUCCESS:
            return {
                ...state,
                reviews: payload.reviews
            }

        case FILTER_REVIEW_FAIL:
            return {
                ...state,
            }


        default:
            return state
    };
};

