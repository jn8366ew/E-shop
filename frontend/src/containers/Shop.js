import React, { useState, useEffect} from 'react';
import { connect } from 'react-redux';
import { get_products, get_filtered_products } from "../actions/products";
import { get_categories } from "../actions/categories";
import Card from "../components/Card";
import { prices } from "../helpers/fixedPrices"


const Shop = ({
    categories,
    get_categories,
    products,
    get_products,
    filtered_products,
    get_filtered_products
}) => {
    const [filtered, setFiltered] = useState(false);
    const [formData, setFormData] = useState({
        category_id: '0',
        price_range: 'Any',
    });

    const { category_id, price_range} = formData;

    useEffect(() => {
        get_categories();
        get_products();
        window.scrollTo(0, 0);
    }, []);

    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });

    const onSubmit = e => {
        e.preventDefault();
        window.scrollTo(0, 0);

        // 필터 상태(state) 갱신
        // get_filtered_products
        setFiltered(true)
    };

    const showProducts = () => {
        let results = [];
        let display = [];

        if (
            filtered_products &&
            filtered_products !== null &&
            filtered_products !== undefined &&
            filtered_products
        )   {
                filtered_products.map((product, index) => {
                    return display.push(
                        <div key={index} className='col-4'>
                            <Card
                                product={product}
                            />
                        </div>
                    )
                });
            }
        else if (
            !filtered &&
            products &&
            products !== null &&
            products !== undefined
        )   {
                products.map((product, index) => {
                    return display.push(
                        <div key={index} className='col-4'>
                            <Card
                                product={product}
                            />
                        </div>
                    );
                });
            }

        for (let i = 0; i < display.length; i += 3 ) {
            results.push(<div key={i} className='row'>
                {display[i] ? display[i] : <div className='col-4'></div>}
                {display[i+1] ? display[i+1] : <div className='col-4'></div>}
                {display[i+2] ? display[i+2] : <div className='col-4'></div>}
            </div>)
        }

        return results;
    };


    return (
        <div className='container'>
            <div className='jumbotron mt-5'>
                <h1 className='display-4'>Shop Page</h1>
                <p className='lead'>
                    className lead!
                </p>
            </div>
            <div className='row'>
                <div className='col-2'>
                    <form className='mb-5' onSubmit={e => onSubmit(e)}>
                        <h5>Categories</h5>
                            <div className='form-check'>

                                {/*Bring all category*/}
                                <input
                                    onChange={e => onChange(e)}
                                    value={'0'}
                                    name='category_id'
                                    type='radio'
                                    className='form-check-input'
                                    defaultChecked
                                />
                                <label className='form-check-label'>All</label>
                            </div>

                        {/*Making radio buttons for categories */}

                        {
                            categories &&
                            categories !== null &&
                            categories !== undefined &&
                            categories.map(category => {
                                if (category.sub_categories.length === 0) {
                                    return (
                                        <div key={category.id} className='form-check'>
                                            <input
                                                onChange={e => onChange(e)}
                                                value={category.id.toString()}
                                                name='category_id'
                                                type='radio'
                                                className='form-check-input'
                                            />
                                            <label className='form-check-label'>
                                                {category.name}
                                            </label>
                                        </div>
                                    );
                                } else {
                                    let result = [];
                                    result.push(
                                        <div key={category.id} className='form-check'>
                                            <input
                                                onChange={e => onChange(e)}
                                                value={category.id.toString()}
                                                name='category_id'
                                                type='radio'
                                                className='form-check-input'
                                            />
                                            <label className='form-check-label'>
                                                {category.name}
                                            </label>
                                        </div>
                                    );

                                    category.sub_categories.map(sub_category => {
                                       result.push(
                                           <div key={sub_category.id} className='form-check ml-4'>
                                               <input
                                                   onChange={e => onChange(e)}
                                                   value={sub_category.id.toString()}
                                                   name='category_id'
                                                   type='radio'
                                                   className='form-check-input'
                                               />
                                               <label className='form-check-label'>
                                                   {sub_category.name}
                                               </label>
                                           </div>
                                       );
                                    });

                                    return result;
                                }
                            })

                        }

                        <h5 className='mt-3'>Price Range</h5>
                        {
                            prices && prices.map((price, index) => {
                                if (price.id === 0) {
                                    return (
                                        <div key={index} className='form-check'>
                                            <input
                                               onChange={e => onChange(e)}
                                               value={price.name}
                                               name='price_range'
                                               type='radio'
                                               className='form-check-input'
                                               defaultChecked
                                            />
                                            <label className='form-check-label'>{price.name}</label>
                                        </div>
                                    )
                                } else {
                                    return (
                                        <div key={index} className='form-check'>
                                            <input
                                                onChange={e => onChange(e)}
                                                value={price.name}
                                                name='price_range'
                                                type='radio'
                                                className='form-check-input'
                                            />
                                            <label className='form-check-label'>{price.name}</label>
                                        </div>
                                    )
                                }
                            })
                        }

                        <button className='btn btn-success mt-3'>
                            Update
                        </button>
                    </form>
                </div>
                <div className='col-10'>
                    {showProducts()}
                </div>
            </div>
        </div>
    );
};


const mapStateToProps = state => ({
    categories: state.categories.categories,
    products: state.products.products,
    filtered_products: state.products.filtered_products
});

export default connect(mapStateToProps,
    {
        get_categories,
        get_products,
        get_filtered_products
    })(Shop);