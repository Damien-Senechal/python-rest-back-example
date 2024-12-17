from flask import Blueprint, request, jsonify
from models.database import db
from models.stock import Stock

stock_routes = Blueprint("stock_routes", __name__)

@stock_routes.route("/stocks", methods=["GET"])
def get_stocks():
    try:
        stocks = Stock.query.all()
        return jsonify([stock.to_dict() for stock in stocks]), 200
    except Exception as e:
        return jsonify({"error": "Erreur lors de la récupération des stocks"}), 500