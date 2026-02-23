import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Professional UI for a Director-level tool
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Remi's Strategic Yield Calculator</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: -apple-system, sans-serif; max-width: 600px; margin: 40px auto; line-height: 1.6; padding: 20px; color: #333; }
        .card { border: 1px solid #eaeaea; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        input { width: 100%; padding: 12px; margin: 10px 0 20px 0; border: 1px solid #ddd; border-radius: 6px; box-sizing: border-box; font-size: 16px; }
        button { background: #0070f3; color: white; border: none; padding: 14px; border-radius: 6px; cursor: pointer; width: 100%; font-size: 16px; font-weight: 600; }
        .result { background: #f0f7ff; padding: 20px; margin-top: 25px; border-radius: 8px; border-left: 5px solid #0070f3; }
        .badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; margin-bottom: 10px; }
        .high { background: #e6fffa; color: #234e52; }
        .standard { background: #fffaf0; color: #7b341e; }
    </style>
</head>
<body>
    <div class="card">
        <h2>UK Property Yield Calculator</h2>
        <p>Enter details to assess the strategic value of a residential asset.</p>
        <form method="POST">
            <label>Property Purchase Price (£)</label>
            <input type="number" name="price" placeholder="e.g. 250000" required>
            <label>Expected Monthly Rent (£)</label>
            <input type="number" name="rent" placeholder="e.g. 1200" required>
            <button type="submit">Calculate Strategic Yield</button>
        </form>
        
        {% if yield_val %}
        <div class="result">
            <div class="badge {{ 'high' if quality == 'High' else 'standard' }}">
                {{ quality }} PERFORMANCE
            </div>
            <br>
            <strong>Gross Annual Yield: {{ yield_val }}%</strong><br>
            <p><em>Director's Assessment:</em> In the 2026 UK market, a yield of {{ yield_val }}% suggests this asset is {{ 'suitable for high-growth portfolio expansion.' if quality == 'High' else 'a stable, wealth-preservation asset.' }}</p>
        </div>
        <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
        <p><small>Next Step: Would you like a breakdown of Stamp Duty for this price point?</small></p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def calculator():
    yield_val = None
    quality = ""
    if request.method == 'POST':
        try:
            price = float(request.form.get('price'))
            rent = float(request.form.get('rent'))
            # Annual Rent / Purchase Price * 100
            yield_val = round(((rent * 12) / price) * 100, 2)
            # 2026 UK Benchmark: Over 6% is high performance for residential
            quality = "High" if yield_val >= 6.0 else "Standard"
        except:
            pass
        
    return render_template_string(HTML_TEMPLATE, yield_val=yield_val, quality=quality)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
