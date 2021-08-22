import React from 'react'

const shippingForm = ({
    full_name,
    address_line_1,
    address_line_2,
    city,
    state_province_region,
    postal_zip_code,
    country_region,
    countries,
    telephone_number,
    onChange,
    buy,
    renderShipping,
    renderPaymentInfo
}) => (
    <form className='mt-5' onSubmit={e => buy(e)}>
        <h4 className='text-muted mb-3'>
            Select Shipping Option:
        </h4>
        {renderShipping()}
        <h5>Shipping Address:</h5>
        <div className='form-group'>
            <label htmlFor='full_name'>Full Name*</label>
            <input
                className='form-control'
                type='text'
                name='full_name'
                placeholder='Full Name'
                onChange={e => onChange(e)}
                value={full_name}
                required
            />
        </div>
        <div className='form-group'>
            <label htmlFor='address_line_1'>Address Line 1*</label>
            <input
                className='form-control'
                type='text'
                name='address_line_1'
                placeholder='Address Line 1'
                onChange={e => onChange(e)}
                value={address_line_1}
                required
            />
        </div>
        <div className='form-group'>
            <label htmlFor='address_line_2'>Address Line 2</label>
            <input
                className='form-control'
                type='text'
                name='address_line_2'
                placeholder='Address Line 2'
                onChange={e => onChange(e)}
                value={address_line_2}
                required
            />
        </div>
        <div className='form-group'>
            <label htmlFor='city'>City*</label>
            <input
                className='form-control'
                type='text'
                name='city'
                placeholder='City'
                onChange={e => onChange(e)}
                value={city}
                required
            />
        </div>
        <div className='form-group'>
            <label htmlFor='state_province_region'>State/Province/Region*</label>
            <input
                className='form-control'
                type='text'
                name='state_province_region'
                placeholder='State/Province/Region'
                onChange={e => onChange(e)}
                value={state_province_region}
                required
            />
        </div>
        <div className='form-group'>
            <label htmlFor='postal_zip_code'>Postal/Zip Code*</label>
            <input
                className='form-control'
                type='text'
                name='postal_zip_code'
                placeholder='Postal/Zip Code'
                onChange={e => onChange(e)}
                value={postal_zip_code}
                required
            />
        </div>

        <div className='form-group'>
            <label htmlFor='country_region'>Country/Region*</label>
            <select
                className='form-control'
                id='country_region'
                name='country_region'
                onChange={e => onChange(e)}
            >
                <option value='Korea, (the Republic of), South'>Korea, (the Republic of), South</option>
                {
                    countries &&
                    countries !== null &&
                    countries !== undefined &&
                    countries.map((country, index) => (
                        <option key={index} value={country.name}>
                            {country.name}
                        </option>
                    ))
                }
            </select>
        </div>

        <div className='form-group'>
            <label htmlFor='telephone_number'>Phone Number*</label>
            <input
                className='form-control'
                type='text'
                name='telephone_number'
                placeholder='telephone_number'
                onChange={e => onChange(e)}
                value={telephone_number}
                required
            />
        </div>

        {renderPaymentInfo()}
    </form>
);

export default shippingForm;