from datetime import date

from extensions import db


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)

    merchant = db.Column(db.String(150), nullable=False)

    amount = db.Column(db.Float, nullable=False)

    date = db.Column(
        db.Date,
        nullable=False,
        default=date.today
    )

    type = db.Column(
        db.String(20),
        nullable=False
    )   # credit or debit

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
            "merchant": self.merchant,
            "amount": self.amount,
            "date": self.date.isoformat(),
            "type": self.type,
            "category": self.category.name if self.category else None,
            "user_id": self.user_id,
        }