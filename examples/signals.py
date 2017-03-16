from dispatcher import Signal


ORDER_CREATED = Signal('order_created', ('order_id', 'user_id', 'shop_id'))
