import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Remi's Strategic Asset Tool</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: -apple-system, sans-serif; max-width: 600px; margin: 40px auto; line-height: 1.6; padding: 20px; color: #333; background-color: #fcfcfc; }
        .card { background: white; border: 1px solid #eaeaea; padding: 30px; border-radius: 12px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
        input, select { width: 100%; padding: 12px; margin: 10px 0 20px 0; border: 1px solid #ddd; border-radius: 6px; box-sizing: border-box; font-size: 16px; }
        button { background: #0070f3; color: white; border: none; padding: 14px; border-radius: 6px; cursor: pointer; width: 100%; font-size: 16px; font-weight: 600; transition: 0.2s; }
        button:hover { background: #0056b3; }
        .result-box { background: #f0f7ff; padding: 25px; margin-top: 25px; border-radius: 8px; border-left: 5px solid #0070f3; }
        .tax-line { display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 15px; }
        .total-tax { font-size: 20px; font-weight: bold; color: #d32f2f; margin-top: 10px; border-top: 1px solid #ddd; padding-top: 10px; }
        .badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; margin-bottom: 15px; background: #e6fffa; color: #234e52; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Strategic Asset Assessment</h2>
        <p>Assess yield and tax liability for UK residential property (2026 Rules).</p>
        <form method="POST">
            <label>Property Price (£)</label>
            <input type="number" name="price" placeholder="e.g. 350000" required>
            <label>Expected Monthly Rent (£)</label>
            <input type="number" name="rent" placeholder="e.g. 1500" required>
            <label>Purchase Type</label>
            <select name="buyer_type">
                <option value="standard">Main Residence (Mover)</option>
                <option value="investment">Investment / 2nd Home (+5% SDLT)</option>
                <option value="ftb">First Time Buyer</option>
            </select>
            <button type="submit">Analyze Asset</button>
        </form>
        
        {% if yield_val %}
        <div class="result-box">
            <div class="badge">FINANCIAL SUMMARY</div>
            <div class="tax-line"><span>Gross Annual Yield:</span> <strong>{{ yield_val }}%</strong></div>
            <div class="tax-line"><span>Total Stamp Duty (SDLT):</span> <strong style="color:#d32f2f;">£{{ "{:,}".format(sdlt) }}</strong></div>
            
            <div class="total-tax">
                Net Day 1 Capital Outlay: £{{ "{:,}".format(price + sdlt) }}
            </div>
            <p><small><em>Director's Note:</em> In 2026, the tax-inclusive cost is vital for calculating your true ROI. Ensure your bridge income covers the initial SDLT.</small></p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

def calculate_sdlt(price, buyer_type):
    # 2026 England/NI Rates
    tax = 0
    surcharge = 0.05 if buyer_type == 'investment' else 0.0
    
    # First Time Buyer Relief Logic
    if buyer_type == 'ftb' and price <= 500000:
        if price > 300000:
            tax += (price - 300000) * 0.05
        return int(tax)

    # Standard / Investment Progressive Calculation
    bands = [
        (125000, 0.00 + surcharge),
        (250000, 0.02 + surcharge),
        (925000, 0.05 + surcharge),
        (1500000, 0.10 + surcharge),
        (float('inf'), 0.12 + surcharge)
    ]
    
    prev_limit = 0
    for limit, rate in bands:
        if price > prev_limit:
            taxable_in_band = min(price, limit) - prev_limit
            tax += taxable_in_band * rate
            prev_limit = limit
        else:
            break
            
    return int(tax)

@app.route('/', methods=['GET', 'POST'])
def assessment():
    res = {}
    if request.method == 'POST':
        price = float(request.form.get('price'))
        rent = float(request.form.get('rent'))
        buyer_type = request.form.get('buyer_type')
        
        res['price'] = price
        res['yield_val'] = round(((rent * 12) / price) * 100, 2)
        res['sdlt'] = calculate_sdlt(price, buyer_type)
        
    return render_template_string(HTML_TEMPLATE, **res)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
