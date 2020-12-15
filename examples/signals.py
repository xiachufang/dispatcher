from dispatcher import Signal


ORDER_CREATED = Signal('order_created', ('order_id', 'user_id', 'shop_id'))

SIGNAL_A= Signal('signal_a', ('order_id', 'user_id'))

SIGNAL_B = Signal('signal_b', ('order_id', 'user_id'))