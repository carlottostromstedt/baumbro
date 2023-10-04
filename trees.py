def find_nearest_tree(user_lat, user_lon):
    query = "SELECT tree_id, tree_name, tree_lat, tree_lon, " \
            "SQRT(POWER(tree_lat - :user_lat, 2) + POWER(tree_lon - :user_lon, 2)) AS distance" \
            "FROM trees " \
            "ORDER BY distance " \
            "LIMIT 1"
    
    result = db.execute(query, {'user_lat': user_lat, 'user_lon': user_lon}).fetchone()
    return result
