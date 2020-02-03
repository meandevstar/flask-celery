"""Usage related models and database functionality"""
from decimal import Decimal
from sqlalchemy.sql import func

from src.models.base import db
from src.models.cycles import BillingCycle
from src.constants import SubscriptionStatus


class DataUsage(db.Model):
    """Model class to represent data usage record

    Note:
        A daily usage record is created for a subscription each day
        it is active, beginning at midnight UTC timezone.

    """
    __tablename__ = "data_usages"

    id = db.Column(db.Integer, primary_key=True)
    mb_used = db.Column(db.Float, default=0.0)
    from_date = db.Column(db.TIMESTAMP(timezone=True))
    to_date = db.Column(db.TIMESTAMP(timezone=True))

    subscription_id = db.Column(
        db.Integer, db.ForeignKey("subscriptions.id"), nullable=False
    )
    subscription = db.relationship("Subscription", back_populates="data_usages")

    def __repr__(self):  # pragma: no cover
        return (
            f"<{self.__class__.__name__}: {self.id} ({self.subscription_id}) "
            f"{self.mb_used} MB {self.from_date} - {self.to_date}>"
        )

    @classmethod
    def get_statistics_for_a_subscription(cls, sid, date=None):
        """Helper method to get data usage on billing cycle of given date

        Args:
            sid (int): subscription id to look up
            date (date): date to get billing cycle for

        Returns:
            dict: {
                over_limit,      true if data usage is over plan limit
                amount_used,     the amount of data used in megabytes
                amount_left      amount used over plan limit in megabytes
            }

        """
        cycle = BillingCycle.get_current_cycle(date)
        default_usage = cls.query \
            .filter(cls.subscription_id == sid) \
            .first()
        subscription = default_usage is not None and default_usage.subscription
        plan = default_usage is not None and default_usage.subscription.plan

        # get total amount used in current cycle
        query = []
        query.append(cls.subscription_id == sid)

        if cycle is not None:
            query.append(cls.from_date >= cycle.start_date)
            query.append(cls.to_date <= cycle.end_date)

        amount = cls.query \
            .with_entities(func.sum(cls.mb_used)) \
            .filter(*query) \
            .scalar()

        if plan and subscription and subscription.status != SubscriptionStatus.new:
            mb_available = plan.mb_available - amount
        else:
            mb_available = 0

        return {
            "over_limit": mb_available <= 0,
            "amount_used": amount,
            "amount_left": mb_available if mb_available > 0 else 0
        }