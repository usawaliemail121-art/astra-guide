with open("index.html", "r") as f:
    h = f.read()

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
    print("PATCHED: buy() updated with fresh payment links")
else:
    # Try to find existing PAYMENT_LINKS block
    old_links_start = h.find('function buy(plan) {')
    if old_links_start >= 0:
        old_links_end = h.find('\n}', old_links_start) + 2
        h = h[:old_links_start] + new_buy + h[old_links_end:]
        print("PATCHED: buy() replaced (fallback method)")
    else:
        print("ERROR: Could not find buy() function")

with open("index.html", "w") as f:
    f.write(h)
