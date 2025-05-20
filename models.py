from .app import db

class Operator(db.Model):
    __tablename__ = 'operators'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    side = db.Column(db.Text, nullable=False) # attacker or defender
    ability = db.Column(db.Text, nullable=False)
    secondary_gadgets = db.Column(db.Text) # divided by comma
    armor = db.Column(db.Integer) # 1 | 2 | 3
    speed = db.Column(db.Integer) # 1 | 2 | 3
    role = db.Column(db.Text)
    short_bio = db.Column(db.Text) # 2-3 sentences summary
    synergy_examples = db.Column(db.Text) # divided by comma
    counter_examples = db.Column(db.Text) # divided by comma
    solo_friendly = db.Column(db.Boolean)

    def __repr__(self):
        return f"<Operator {self.name} ({self.side})>"

    # serialisation, might be used for JSON
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'side': self.side,
            'ability': self.ability,
            'secondary_gadgets': self.secondary_gadgets,
            'armor': self.armor,
            'speed': self.speed,
            'role': self.role,
            'short_bio': self.short_bio,
            'synergy_examples': self.synergy_examples,
            'counter_examples': self.counter_examples,
            'solo_friendly': self.solo_friendly
        }

class Map(db.Model):
    __tablename__ = 'maps'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    image_url = db.Column(db.Text, nullable=False)
    defender_sites = db.Column(db.Text, nullable=False)
    electricity_needed = db.Column(db.Boolean, nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f"<Map {self.name}>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'image_url': self.image_url,
            'defender_sites': self.defender_sites,
            'electricity_needed': self.electricity_needed,
            'description': self.description
        }


class GameInfo(db.Model):
    __tablename__ = 'game_info'
    id = db.Column(db.Integer, primary_key=True)
    section_title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<GameInfo {self.section_title}>'
