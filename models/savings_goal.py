from datetime import date

from extensions import db


class SavingsGoal(db.Model):
    __tablename__ = "savings_goals"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(150),
        nullable=False
    )

    target_amount = db.Column(
        db.Float,
        nullable=False
    )

    saved_amount = db.Column(
        db.Float,
        nullable=False,
        default=0.0
    )

    color = db.Column(
        db.String(20),
        nullable=False
    )

    deadline = db.Column(db.Date)

    note = db.Column(db.Text)

    created_at = db.Column(
        db.Date,
        default=date.today
    )

    # Foreign Key
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # Relationship
    user = db.relationship(
        "User",
        back_populates="savings_goals"
    )

    def to_dict(self):
        progress = (
            (self.saved_amount / self.target_amount) * 100
            if self.target_amount > 0
            else 0
        )

        return {
            "id": self.id,
            "name": self.name,
            "target_amount": self.target_amount,
            "saved_amount": self.saved_amount,
            "color": self.color,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "note": self.note,
            "progress": round(progress, 1),
            "user_id": self.user_id
        }

    def __repr__(self):
        return f"<SavingsGoal {self.name}>"