"""Subscription resource for handling any subscription requests"""
from flask import jsonify
from webargs import fields
from webargs.flaskparser import use_kwargs
from flask_restful import Resource
from datetime import datetime

from src.models.subscriptions import Subscription
from src.models.utils import get_object_or_404, convert_mb_to_gb
from src.models.usages import DataUsage
from src.schemas.subscriptions import SubscriptionSchema

from src.tasks import check_data_blocks


class SubscriptionAPI(Resource):
    """Resource/routes for subscription endpoints"""

    def get(self, sid):
        """External facing subscription endpoint GET

        Gets an existing Subscription object by id

        Args:
            sid (int): id of subscription object

        Returns:
            json: serialized subscription object

        """
        subscription = get_object_or_404(Subscription, sid)
        result = SubscriptionSchema().dump(subscription)
        return jsonify(result.data)


class SubscriptionListAPI(Resource):
    """Resource/routes for subscriptions endpoints"""

    @use_kwargs(SubscriptionSchema(partial=True), locations=("query",))
    def get(self, **kwargs):
        """External facing subscription list endpoint GET

        Gets a list of Subscription object with given args

        Args:
            kwargs (dict): filters to apply to query Subscriptions

        Returns:
            json: serialized list of Subscription objects

        """
        subscriptions = Subscription.get_subscriptions(**kwargs)
        result = SubscriptionSchema().dump(subscriptions, many=True)
        return jsonify(result.data)

class SubscriptionDataUsageAPI(Resource):
    """Resource/routes for subscription endpoints"""

    def get(self, sid, date=None):
        """Subscription data usage endpoint GET

        Gets the amount of data usage for a given subscription in gigabytes for the current billing cycle

        Args:
            sid (int): id of subscription to analyse

        Returns:
            json: {
                over_limit,      true if data usage is over plan limit
                amount_used,     the amount of data used in megabytes
                amount_left      amount used over plan limit in megabytes
            }

        """
        
        date = datetime(2019, 9, 16)

        statistics = DataUsage.get_statistics_for_a_subscription(sid=sid, date=date)
        statistics["amount_used"] = convert_mb_to_gb(statistics.get("amount_used"))
        statistics["amount_left"] = convert_mb_to_gb(statistics.get("amount_left"))
        return jsonify(statistics)
