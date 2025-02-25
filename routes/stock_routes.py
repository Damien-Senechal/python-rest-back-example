from flask import Blueprint, json, request, jsonify
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

@stock_routes.route("/stocks/<int:stock_id>", methods=["GET"])
def get_stock(stock_id):
    stock = db.session.get(Stock, stock_id)
    if not stock:
        return jsonify({"error": "Stock not found"}), 404
    return jsonify(stock.to_dict()), 200


@stock_routes.route("/stocks", methods=["POST"])
def create_stock():
    data = request.get_json()
    if not data.get("name") or not data.get("quantity") or not data.get("price"):
        return jsonify({"error": "Name, quantity and price are required"}), 400

    if Stock.query.filter_by(name=data["name"]).first():
        return jsonify({"error": "This ingredient already exists in stock"}), 400

    new_stock = Stock(name=data["name"], quantity=data["quantity"], price=data["price"])
    db.session.add(new_stock)
    db.session.commit()
    return jsonify(new_stock.to_dict()), 201

@stock_routes.route("/stocks/<int:stock_id>", methods=["PUT"])
def update_stock(stock_id):
    stock = Stock.query.get(stock_id)
    if not stock:
        return jsonify({"error": "Stock not found"}), 404

    data = request.get_json()
    stock.name = data.get("name", stock.name)
    stock.quantity = data.get("quantity", stock.quantity)
    stock.price = data.get("price", stock.price)
    db.session.commit()
    return jsonify(stock.to_dict()), 200

# DELETE /stocks/<int:stock_id> - Delete a stock entry
@stock_routes.route("/stocks/<int:stock_id>", methods=["DELETE"])
def delete_stock(stock_id):
    stock = Stock.query.get(stock_id)
    if not stock:
        return jsonify({"error": "Stock not found"}), 404

    db.session.delete(stock)
    db.session.commit()
    return jsonify({"message": "Stock deleted successfully"}), 200
