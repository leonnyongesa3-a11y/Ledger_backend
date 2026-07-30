from datetime import datetime

from extensions import db


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)

    amount = db.Column(db.Float, nullable=False)

    type = db.Column(db.String(20), nullable=False)
    # Expected values: "Income" or "Expense"

    date = db.Column(
        db.Date,
        nullable=False,
        default=datetime.utcnow
    )

    description = db.Column(db.Text)

    # Foreign Keys
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=False
    )

    # Relationships
    user = db.relationship(
        "User",
        back_populates="transactions"
    )

    category = db.relationship(
        "Category",
        back_populates="transactions"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "amount": self.amount,
            "type": self.type,
            "date": self.date.isoformat(),
            "description": self.description,
            "user_id": self.user_id,
            "category_id": self.category_id
        }

    def __repr__(self):
        return f"<Transaction {self.title}>"