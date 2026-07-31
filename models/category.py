from extensions import db


class Category(db.Model):
    __tablename__ = "categories"

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "name",
            name="unique_category_per_user"
        ),
    )


    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="categories"
    )

    transactions = db.relationship(
        "Transaction",
        back_populates="category",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id
        }

    def __repr__(self):
        return f"<Category {self.name}>"