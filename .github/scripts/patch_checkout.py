with open("index.html", "r") as f:
    h = f.read()

# Remove the unnecessary Razorpay checkout.js script tag
old_script = '<script src="https://checkout.razorpay.com/v1/checkout.js"></script>'
if old_script in h:
    h = h.replace(old_script, '')
    print("REMOVED: Razorpay checkout.js script tag")
else:
    print("SKIP: checkout.js tag not found (already removed)")

# Ensure buy() uses payment links
old_buy_start = 'function buy(plan) {'
old_buy_end = 'rzp.open();\n}'

new_buy = '''function buy(plan) {
  const PAYMENT_LINKS = {
    digital: "https://rzp.io/rzp/A1AMi3Op",
    combo: "https://rzp.io/rzp/QyhGDWBb"
  };
  const link = PAYMENT_LINKS[plan] || PAYMENT_LINKS.digital;
  window.location.href = link;
}'''

start_idx = h.find(old_buy_start)
end_idx = h.find(old_buy_end, start_idx)
if start_idx >= 0 and end_idx >= 0:
    end_idx += len(old_buy_end)
    h = h[:start_idx] + new_buy + h[end_idx:]
    print("PATCHED: buy() uses payment links")
else:
    # Check if already using PAYMENT_LINKS
    if 'PAYMENT_LINKS' in h:
        print("OK: buy() already uses payment links")
    else:
        print("ERROR: Could not find buy() function")

with open("index.html", "w") as f:
    f.write(h)
