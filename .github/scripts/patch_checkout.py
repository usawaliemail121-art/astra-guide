with open("index.html", "r") as f:
    h = f.read()

old_theme = 'theme: { color: "#0a1628" }\n  };'
new_theme = 'theme: { color: "#0a1628" },\n    modal: {\n      ondismiss: function() {\n        document.querySelectorAll(".razorpay-container, .razorpay-backdrop, iframe[data-rzp]").forEach(function(el) { el.remove(); });\n        document.body.style.removeProperty("overflow");\n        document.body.style.removeProperty("position");\n      },\n      escape: true,\n      backdropclose: true\n    },\n    retry: {\n      enabled: true,\n      max_count: 3\n    }\n  };'

if old_theme in h:
    h = h.replace(old_theme, new_theme)
    print("PATCHED: modal+retry added")
else:
    print("SKIP: theme block not found")

old_fail = 'setTimeout(function(){ try{ rzp.close(); }catch(e){} alert("Payment failed. Please try again."); }, 300);'
new_fail = 'console.log("Payment failed:", resp.error);\n    try { rzp.close(); } catch(e) {}\n    setTimeout(function() {\n      document.querySelectorAll(".razorpay-container, .razorpay-backdrop, iframe[data-rzp]").forEach(function(el) { el.remove(); });\n      document.body.style.removeProperty("overflow");\n      document.body.style.removeProperty("position");\n      alert("Payment failed. Please try again.");\n    }, 500);'

if old_fail in h:
    h = h.replace(old_fail, new_fail)
    print("PATCHED: failure handler improved")
else:
    print("SKIP: failure handler not found")

with open("index.html", "w") as f:
    f.write(h)
