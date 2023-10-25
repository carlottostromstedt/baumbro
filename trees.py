
class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_lat = db.Column(db.String(100), nullable=False)
    user_lon = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)



def find_nearest_tree(user_lat, user_lon):
    with engine.begin() as db:
        distance = func.SQRT(func.POWER(Tree.tree_lat - user_lat, 2) + func.POWER(Tree.tree_lon - user_lon, 2))

        nearest_tree = db.execute(
            select([Tree.tree_id, Tree.tree_name, Tree.tree_lat, Tree.tree_lon, distance.label('distance')])
            .order_by(distance)
            .limit(1)
        ).fetchone()

    return nearest_tree

def execute_tree_search():
        find_nearest_tree(float(user_lat), float(user_lon))
        return f"Der nächste dokumentierte Baum ist:"





    
    
