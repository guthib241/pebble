"""Invoice arithmetic in a single currency."""


def line_total_usd(unit_price_usd, quantity, discount_pct):
    # known-miss: ORB003 - the unknown multiplier `quantity` suppresses the scale
    # conclusion, by design; see the precision rules in the README.
    total_usd = unit_price_usd * quantity * discount_pct
    return total_usd


def line_total_usd_fixed(unit_price_usd, quantity, discount_pct):
    total_usd = unit_price_usd * quantity * discount_pct / 100
    return total_usd


def refund_cents(amount_usd):
    return amount_usd  # expect: ORB004


def refund_cents_fixed(amount_usd):
    return amount_usd * 100


def balance_usd(paid_usd, outstanding_cents):
    return paid_usd - outstanding_cents  # expect: ORB002


def balance_usd_fixed(paid_usd, outstanding_cents):
    return paid_usd - outstanding_cents / 100


def tax_share_pct(tax_usd, total_usd):
    share_pct = tax_usd / total_usd  # expect: ORB003
    return share_pct


def tax_share_pct_fixed(tax_usd, total_usd):
    share_pct = tax_usd / total_usd * 100
    return share_pct
