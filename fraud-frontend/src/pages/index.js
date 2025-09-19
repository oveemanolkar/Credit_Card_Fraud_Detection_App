import { useState } from 'react';

export default function Home() {
  const [form, setForm] = useState({
    Amount: '',
    Country: '',
    TimeOfDay: '',
    MerchantType: '',
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    try {
      // ✅ Use ONLY env variable, no localhost fallback
      const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
      console.log('Calling backend at:', backendUrl);

      const res = await fetch(`${backendUrl}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          Amount: parseFloat(form.Amount),
          Country: form.Country,
          TimeOfDay: form.TimeOfDay.toLowerCase(),
          MerchantType: form.MerchantType.toLowerCase(),
        }),
      });

      const data = await res.json();

      if (data.error) {
        setResult(`Error: ${data.error}`);
      } else {
        setResult(data.message); // "Fraud" or "Not Fraud"
      }
    } catch (error) {
      console.error('Fetch error:', error);
      setResult('Error connecting to backend.');
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center px-4">
      <div className="bg-white rounded-2xl shadow-lg p-8 w-full max-w-md">
        <h1 className="text-2xl font-bold text-center mb-6 text-indigo-700">
          🧠 Credit Card Fraud Detector
        </h1>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Amount</label>
            <input
              name="Amount"
              type="number"
              value={form.Amount}
              onChange={handleChange}
              required
              className="w-full border px-3 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-400"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Country</label>
            <select
              name="Country"
              onChange={handleChange}
              value={form.Country}
              required
              className="w-full border px-3 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-400"
            >
              <option value="">Select</option>
              <option value="US">US</option>
              <option value="UK">UK</option>
              <option value="IN">IN</option>
              <option value="AU">AU</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Time of Day</label>
            <select
              name="TimeOfDay"
              onChange={handleChange}
              value={form.TimeOfDay}
              required
              className="w-full border px-3 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-400"
            >
              <option value="">Select</option>
              <option value="morning">Morning</option>
              <option value="afternoon">Afternoon</option>
              <option value="evening">Evening</option>
              <option value="night">Night</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Merchant Type</label>
            <select
              name="MerchantType"
              onChange={handleChange}
              value={form.MerchantType}
              required
              className="w-full border px-3 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-400"
            >
              <option value="">Select</option>
              <option value="online">Online</option>
              <option value="grocery">Grocery</option>
              <option value="travel">Travel</option>
              <option value="electronics">Electronics</option>
            </select>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-md transition"
          >
            {loading ? 'Predicting...' : 'Predict'}
          </button>
        </form>

        {result && (
          <div className="mt-6 text-center text-lg font-semibold text-gray-700">
            Prediction: <span className="text-indigo-600">{result}</span>
          </div>
        )}
      </div>
    </div>
  );
}
