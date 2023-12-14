import os
import psycopg2
from __init__ import app
from __init__ import db
from app.region_routes import region_bp
from app.tax_param_route import car_2_bp
from app.tax_route import car_bp


app.register_blueprint(region_bp)
app.register_blueprint(car_bp)
app.register_blueprint(car_2_bp)


if __name__ == '__main__':
    try:
        with app.app_context():
            db.create_all()
            print('ok')
    except Exception as e:
        print(f"Error during table creation: {str(e)}")
    app.run(debug=True)