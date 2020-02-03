import celery

from src.models.base import db
from src.models.subscriptions import Subscription
from src.models.usages import DataUsage
from src.models.service_codes import ServiceCode
from src.constants import SubscriptionStatus


@celery.task()
def check_data_blocks():
	print('==> Checking data blocks...')

	codes = {}

	for code in ServiceCode.query.all():
		codes[code.name] = code

	for subscription in Subscription.get_subscriptions():
		data_blocked = codes.get("Data Block") in subscription.service_codes
		is_unlimited = subscription.plan

		# A subscription must be `active`, `suspended`, or `expired` to have any usage data
		if subscription.status != SubscriptionStatus.new:
			statistics = DataUsage.get_statistics_for_a_subscription(subscription.id)
			
			if statistics.get("over_limit") and data_blocked == False:
				subscription.service_codes.append(codes.get("Data Block"))
			
			if statistics.get("over_limit") == False and data_blocked:
					subscription.service_codes.remove(codes.get("Data Block"))

		elif data_blocked == False:
			subscription.service_codes.append(codes.get("Data Block"))
		
		# A subscription should not have the data blocking service code applied if it's on an unlimited plan
		if is_unlimited and data_blocked:
			subscription.service_codes.remove(codes.get("Data Block"))

	db.session.commit()

	print('==> Finished checking data blocks.')