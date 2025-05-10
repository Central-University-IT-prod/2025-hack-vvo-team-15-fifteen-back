from flask import Flask, jsonify, request

app = Flask(__name__)

sightseeingsArray = [
    {
        "name": 'nameTwo',
        "cost": 25.00,
        "type": 'typeOne',
        "city": 'Vdk',
        "street": 'streetOne',
        "house": '5',
    },
    {
        "name": 'nameTwo',
        "cost": 16.00,
        "type": 'typeone',
        "city": 'Vdk',
        "street": 'streetwo',
        "house": '1',
    },
    {
        'name': 'nametwo',
        'cost': 17.00,
        'type': 'tipetwo',
        'city': 'cityone',
        'street': 'streetwo',
        'house': '1',
    },
]

# Массив для хранения пользователей
usersArray = [
    {
        "user_name": "Ivan",
        "user_fename": "Ivanov",
        "user_data": "1990-01-01",
        "user_email": "ivan@example.com",
        "user_pol": "male",
        "user_password": "password123",  # Храните пароли безопасно (в хешированном виде)
        "user_type": 1,
    },
    {
        "user_name": "Maria",
        "user_fename": "Petrova",
        "user_data": "1992-02-02",
        "user_email": "maria@example.com",
        "user_pol": "female",
        "user_password": "mypassword",  # Храните пароли безопасно (в хешированном виде)
        "user_type": 2,
    },
]


@app.route("/")
def sightseeings():
    return jsonify(sightseeingsArray)


@app.route("/filtered")
def filteredSightseeings():
    try:
        city_name = request.args.get('cityName')
        sightseeing_type = request.args.get('type')
        min_cost = request.args.get('minCost', type=float)
        max_cost = request.args.get('maxCost', type=float)

        filtered_sightseeings = sightseeingsArray

        if city_name:
            filtered_sightseeings = [sightseeing for sightseeing in filtered_sightseeings if
                                     sightseeing['city'] == city_name]
        if sightseeing_type:
            filtered_sightseeings = [sightseeing for sightseeing in filtered_sightseeings if
                                     sightseeing['type'] == sightseeing_type]

        if min_cost is not None:
            filtered_sightseeings = [sightseeing for sightseeing in filtered_sightseeings if
                                     sightseeing['cost'] >= min_cost]

        if max_cost is not None:
            filtered_sightseeings = [sightseeing for sightseeing in filtered_sightseeings if
                                     sightseeing['cost'] <= max_cost]

        if not filtered_sightseeings:
            return jsonify({"message": "No sightseeings found matching the criteria"}), 404

        return jsonify(filtered_sightseeings)

    except Exception as e:
        print(f'Error: {e}')
        return jsonify({"message": "An error occurred"}), 500


@app.route("/register", methods=["GET"])
def register():
    data = request.json

    required_fields = ['user_name', 'user_fename', 'user_data', 'user_email', 'user_pol', 'user_password', 'user_type']
    if not all(field in data for field in required_fields):
        return jsonify({"message": "All fields are required"}), 400

    user = {
        "user_name": data['user_name'],
        "user_fename": data['user_fename'],
        "user_data": data['user_data'],
        "user_email": data['user_email'],
        "user_pol": data['user_pol'],
        "user_password": data['user_password'],  # Необходимо реализовать хеширование паролей
        "user_type": data['user_type']
    }

    if user['user_type'] not in [1, 2]:
        return jsonify({"message": "Invalid user type"}), 400

    usersArray.append(user)
    return jsonify({"message": "User registered successfully"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user_email = data.get("user_email")
    user_password = data.get("user_password")

    for user in usersArray:
        if user['user_email'] == user_email and user[
            'user_password'] == user_password:  # Необходимо реализовать хеширование паролей
            return jsonify({"message": "Login successful", "user": user}), 200

    return jsonify({"message": "Invalid credentials"}), 401


if __name__ == "__main__":
    app.run(debug=True)
