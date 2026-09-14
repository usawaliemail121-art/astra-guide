with open("index.html", "r") as f:
    h = f.read()

# Replace the entire buy() function to use Payment Links instead of checkout.js popup
# This avoids the order_id requirement entirely
old_buy_start = 'function buy(plan) {'
old_buy_end = 'rzp.open();\n}'

new_buy = '''function buy(plan) {
  const PAYMENT_LINKS = {
    digital: "https://rzp.io/rzp/UqgmcAU0",
    combo: "https://rzp.io/rzp/L7AaZnA"
  };
  const link = PAYMENT_LINKS[plan] || PAYMENT_LINKS.digital;
  window.location.href = link;
}'''

start_idx = h.find(old_buy_start)
end_idx = h.find(old_buy_end, start_idx)
if start_idx >= 0 and end_idx >= 0:
    end_idx += len(old_buy_end)
    h = h[:start_idx] + new_buy + h[end_idx:]
    print("PATCHED: buy() replaced with Payment Link redirect")
else:
    print("ERROR: Could not find buy() function boundaries")
    print(f"  start found: {start_idx}, end found: {end_idx}")

with open("index.html", "w") as f:
    f.write(h)
