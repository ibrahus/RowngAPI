import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from models import *
import datetime
from auth import *


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    setup_migrations(app)

    '''
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
    # create_and_drop_all()

    CORS(app)

    @app.route('/')
    def health():
        return jsonify("Healthy")

    # Endpoint to get all vendors
    @app.route('/vendors')
    @requires_auth('GET:vendors')
    def retrieve_vendors(payload):
        selection = Vendor.query.order_by(Vendor.id).all()
        if len(selection) == 0:
            return jsonify({
                'success': False,
                'message': 'Vendor not exist'
            }), 404
        vendors = [vendor.format() for vendor in selection]

        return jsonify({
            'success': True,
            'vendors': vendors
        })

    # Endpoint to get user bookings
    @app.route('/user-bookings/<int:user_id>')
    @requires_auth('GET:user-booking')
    def retrieve_user_bookings(payload, user_id):
        selection = User.query.filter(User.id == user_id).one_or_none()
        if selection is None:
            return jsonify({
                'success': False,
                'message': 'User not exist'
            }), 404

        user_bookings = [user for user in selection.bookings]

        bookings_list = []
        service_list = []
        for user_booking in user_bookings:
            for service_id in user_booking.services:
                service = Service.query.filter(
                    Service.id == service_id).one_or_none()
                if service is not None:
                    service_dict = {
                        'service_name': service.service_name,
                        'service_price': service.service_price,
                        'service_duration': str(service.service_duration),
                    }
                    service_list.append(service_dict)

            booking_dict = {
                'booking_id': user_booking.id,
                'booking_date': user_booking.booking_date,
                'vendor_name': user_booking.vendor.name,
                'user_name': user_booking.user.name,
                'services': service_list
            }
            bookings_list.append(booking_dict)

        return jsonify({
            'success': True,
            'user_bookings': bookings_list
        })

    # Endpoint to get vendor bookings
    @app.route('/vendor-bookings/<int:vendor_id>')
    @requires_auth('GET:vendor-booking')
    def retrieve_vendor_bookings(payload, vendor_id):
        selection = Vendor.query.filter(Vendor.id == vendor_id).one_or_none()
        if selection is None:
            return jsonify({
                'success': False,
                'message': 'Vendor not exist'
            }), 404

        vendor_bookings = [vendor for vendor in selection.bookings]

        bookings_list = []
        service_list = []
        for vendor_booking in vendor_bookings:
            for service_id in vendor_booking.services:
                service = Service.query.filter(
                    Service.id == service_id).one_or_none()
                if service is not None:
                    service_dict = {
                        'service_name': service.service_name,
                        'service_price': service.service_price,
                        'service_duration': str(service.service_duration),
                    }
                    service_list.append(service_dict)

            booking_dict = {
                'booking_id': vendor_booking.id,
                'booking_date': vendor_booking.booking_date,
                'vendor_name': vendor_booking.vendor.name,
                'user_name': vendor_booking.user.name,
                'services': service_list
            }
            bookings_list.append(booking_dict)

        return jsonify({
            'success': True,
            'vendor_bookings': bookings_list
        })

    # Endpoint to add new booking
    @app.route('/create-booking', methods=['POST'])
    @requires_auth('POST:create-booking')
    def create_booking(payload):
        body = request.get_json()

        try:
            booking = Booking(
                vendor_id=body['vendor_id'],
                user_id=body['user_id'],
                services=body['services'],
                booking_date=datetime.datetime.fromisoformat(
                    body['booking_date']),
            )
            booking.insert()
        except:
            abort(500)

        return jsonify({
            'success': True,
            'booking': booking.format()
        })

    # Endpoint to create a vendor
    @app.route('/create-vendor', methods=['POST'])
    @requires_auth('POST:create-vendor')
    def create_vendor(payload):
        body = request.get_json()

        try:
            vendor = Vendor(
                name=body['name'],
                city=body['city'],
                address=body['address'],
                start_duty_time=datetime.time(body['start_duty_time']),
                end_duty_time=datetime.time(body['end_duty_time']),
            )
            vendor.insert()
        except:
            abort(500)

        return jsonify({
            'success': True,
            'vendor': vendor.format()
        })

    # Endpoint to create a user
    @app.route('/create-user', methods=['POST'])
    @requires_auth('POST:create-user')
    def create_user(payload):
        body = request.get_json()

        try:
            user = User(
                name=body['name'],
                city=body['city'],
            )
            user.insert()
        except:
            abort(500)

        return jsonify({
            'success': True,
            'user': user.format()
        })

    # Endpoint to create a service
    @app.route('/create-service', methods=['POST'])
    @requires_auth('POST:create-service')
    def create_service(payload):
        body = request.get_json()

        try:
            service = Service(
                service_name=body['service_name'],
                service_price=body['service_price'],
                service_duration=datetime.time(body['service_duration']),
                vendor_id=body['vendor_id']
            )
            service.insert()
        except:
            abort(500)

        return jsonify({
            'success': True,
            'service': service.format()
        })

    # Endpoint to update a booking
    @app.route('/update-booking/<int:booking_id>', methods=['PATCH'])
    @requires_auth('PATCH:update-booking')
    def update_booking(payload, booking_id):
        booking = Booking.query.filter(Booking.id == booking_id).one_or_none()
        if booking is None:
            return jsonify({
                'success': False,
                'message': 'Booking not exist'
            }), 404

        body = request.get_json()

        if 'booking_date' in body:
            booking.booking_date = datetime.datetime.fromisoformat(
                body['booking_date'])

        if 'services' in body:
            booking.services = body['services']

        booking.update()

        return jsonify({
            'success': True,
            'booking': booking.format()
        })

    # Endpoint to delete a booking
    @app.route('/delete-booking/<int:booking_id>', methods=['DELETE'])
    @requires_auth('DELETE:delete-booking')
    def delete_booking(payload, booking_id):
        booking = Booking.query.filter(Booking.id == booking_id).one_or_none()
        if booking is None:
            return jsonify({
                'success': False,
                'message': 'Booking not exist'
            }), 404
        booking.delete()

        return jsonify({
            'success': True,
            'deleted': booking.id
        })

    # Error Handling

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        """
        Receive the raised authorization error and propagates it as response
        """
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    @app.errorhandler(Exception)
    def handle_auth_error(ex):
        response = jsonify(message=str(ex))
        response.status_code = (
            ex.code if isinstance(ex, HTTPException) else 500)
        return response

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
