from extensions import db


class Budget(db.Model):
    __tablename__ = "budgets"

    id = db.Column(db.Integer, primary_key=True)

    category = db.Column(
        db.String(100),
        nullable=False
    )

    spent = db.Column(
        db.Float,
        nullable=False,
        default=0.0
    )

    limit_amount = db.Column(
        db.Float,
        nullable=False,
        default=0.0
    )

    color = db.Column(
        db.String(20),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="budgets"
    )

    def to_dict(self):
        progress = (
            (self.spent / self.limit_amount) * 100
            if self.limit_amount > 0
            else 0
        )

        return {
            "id": self.id,
            "category": self.category,
            "spent": self.spent,
            "limit": self.limit_amount,
            "color": self.color,
            "progress": round(progress, 1)
        }

    def __repr__(self):
        return f"<Budget {self.category}>"