import React from 'react';
import { Link } from 'react-router-dom';
import Card from './Card'
import orange_pic from "../assets/orange.png"

const landingPage = ({
    products_arrival,
    products_sold,
    add_item,
    get_items,
    get_total,
    get_item_total,
    setRedirect,
}) => (
    <div className='container'>
        <div className='jumbotron mt-5'
            style={{
                backgroundColor: "transparent",
                backgroundImage: `url(${orange_pic}`
                }}>
            <h1 className='display-4'>Welcome to E-shop!</h1>
            <p className='lead'></p>
            <hr className='my-4' />
            <Link className='btn btn-danger btn-lg' to='/shop'>SHOP NOW</Link>
        </div>

        <section>
            <h2 className='mt-5 mb-5 display-4'>Newest Products</h2>
            <div className='row'>
                {
                    products_arrival &&
                    products_arrival !== null &&
                    products_arrival !== undefined &&
                    products_arrival.map((product, index) => (
                        <div key={index} className='col-4'>
                            <Card
                                product={product}
                                add_item={add_item}
                                get_items={get_items}
                                get_total={get_total}
                                get_item_total={get_item_total}
                                setRedirect={setRedirect}
                            />
                        </div>
                    ))
                }
            </div>
        </section>

        <section>
            <h2 className='mt-5 mb-5 display-4'>Top 3 Products</h2>
            <div className='row'>
                {
                    products_sold &&
                    products_sold !== null &&
                    products_sold !== undefined &&
                    products_sold.map((product, index) => (
                        <div key={index} className='col-4'>
                            <Card
                                product={product}
                                add_item={add_item}
                                get_items={get_items}
                                get_total={get_total}
                                get_item_total={get_item_total}
                                setRedirect={setRedirect}
                            />
                        </div>
                    ))
                }
            </div>


        </section>



    </div>

);

export default landingPage;