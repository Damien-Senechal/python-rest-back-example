import unittest

from flask import json
from app import create_app
from models.database import db
from models.stock import Stock

class StockTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
 
    def test_get_stocks_list(self):

        with self.app.app_context():
            stock1=Stock(name="Crayon", quantity=100, price=0.99)
            stock2=Stock(name="Cahier", quantity=50, price=2.99)
            db.session.add_all([stock1, stock2])
            db.session.commit()

        response = self.client.get("/api/stocks")

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], "Crayon")
        self.assertEqual(data[0]['quantity'], 100)
        self.assertEqual(data[1]['name'], "Cahier")
        self.assertEqual(data[1]['quantity'], 50)

    def test_get_empty_stocks_list(self):
        response = self.client.get("/api/stocks")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 0)

        
    def test_get_stock(self):
        with self.app.app_context():
            stock = Stock(name="Crayon", quantity=100, price=0.99)
            db.session.add(stock)
            db.session.commit()

            stock_id = stock.id

        response = self.client.get(f"/api/stocks/{stock_id}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["name"], "Crayon")
        self.assertEqual(data["quantity"], 100)
        self.assertEqual(data["price"], 0.99)

    def test_get_nonexistent_stock(self):
        response = self.client.get("/api/stocks/999")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
