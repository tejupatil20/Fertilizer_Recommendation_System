import { useState } from 'react'
import Navbar from '../components/Navbar'
import PredictionResult from '../components/PredictionResult'
import api from '../api/axios'
import toast from 'react-hot-toast'
import {
  FlaskConical, Loader2, Info, Sparkles, Sliders, CheckCircle2,
  Layers, Activity, Sun, CloudRain, Snowflake, Sprout, ShoppingBag
} from 'lucide-react'

const CROPS = [
  'Wheat', 'Rice', 'Maize', 'Cotton', 'Sugarcane',
  'Paddy', 'Barley', 'Millets', 'Oil seeds', 'Pulses', 'Ground Nuts', 'Tobacco',
]

// Soil Type Options (Aesthetic cards, no emojis)
const SOIL_TYPES = [
  {
    id: 'loamy',
    name: 'Loamy Soil (Domat Mitti)',
    desc: 'Dark, crumbly, fertile soil — balanced nutrients',
    n: 80, p: 50, k: 60, ph: 6.8,
  },
  {
    id: 'black',
    name: 'Black Soil (Kali Mitti)',
    desc: 'Deep black, holds water well, rich in potassium',
    n: 65, p: 40, k: 120, ph: 7.4,
  },
  {
    id: 'red',
    name: 'Red Soil (Lal Mitti)',
    desc: 'Reddish, porous, lower in nitrogen & phosphorus',
    n: 40, p: 25, k: 50, ph: 5.8,
  },
  {
    id: 'sandy',
    name: 'Sandy Soil (Retili Mitti)',
    desc: 'Light texture, drains fast, lower organic matter',
    n: 30, p: 20, k: 35, ph: 6.2,
  },
  {
    id: 'clayey',
    name: 'Clayey Soil (Chikni Mitti)',
    desc: 'Heavy texture, high moisture & nutrient capacity',
    n: 75, p: 45, k: 90, ph: 7.6,
  },
]

// Plant Health Symptoms (Aesthetic cards)
const LEAF_SYMPTOMS = [
  {
    id: 'healthy',
    name: 'Normal & Healthy',
    desc: 'Dark green leaves, active shoot development',
    nMult: 1.0, pMult: 1.0, kMult: 1.0,
  },
  {
    id: 'yellow',
    name: 'Yellowish Leaves',
    desc: 'Older leaves turning pale yellow (Nitrogen deficiency)',
    nMult: 0.4, pMult: 1.0, kMult: 1.0,
  },
  {
    id: 'purple',
    name: 'Purple / Stunted Leaves',
    desc: 'Purple-tinged foliage or slow root growth (Phosphorus deficiency)',
    nMult: 1.0, pMult: 0.3, kMult: 1.0,
  },
  {
    id: 'brown_tips',
    name: 'Brown Leaf Edges',
    desc: 'Curled or scorched leaf margins (Potassium deficiency)',
    nMult: 1.0, pMult: 1.0, kMult: 0.4,
  },
]

// Season Presets
const SEASONS = [
  { id: 'monsoon', name: 'Monsoon / Rainy Season', temp: 26, humidity: 85, rainfall: 250, icon: <CloudRain size={18} className="text-blue-500" /> },
  { id: 'winter', name: 'Winter / Cool Season', temp: 18, humidity: 60, rainfall: 20, icon: <Snowflake size={18} className="text-cyan-500" /> },
  { id: 'summer', name: 'Summer / Warm Season', temp: 34, humidity: 45, rainfall: 40, icon: <Sun size={18} className="text-amber-500" /> },
]

export default function Predict() {
  const [mode, setMode] = useState('simple') // 'simple' or 'advanced'

  // Simple Mode Choices
  const [selectedCrop, setSelectedCrop] = useState('Wheat')
  const [daysPlanted, setDaysPlanted] = useState(30)
  const [selectedSoil, setSelectedSoil] = useState('loamy')
  const [selectedSymptom, setSelectedSymptom] = useState('healthy')
  const [selectedSeason, setSelectedSeason] = useState('monsoon')

  // Advanced Mode Numerical Inputs
  const [advancedForm, setAdvancedForm] = useState({
    soil_n: 80,
    soil_p: 40,
    soil_k: 40,
    ph: 6.5,
    temperature: 28,
    humidity: 65,
    rainfall: 100,
  })

  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)

  const getPayload = () => {
    if (mode === 'advanced') {
      return {
        crop: selectedCrop,
        days_since_planting: parseInt(daysPlanted),
        soil_n: parseFloat(advancedForm.soil_n),
        soil_p: parseFloat(advancedForm.soil_p),
        soil_k: parseFloat(advancedForm.soil_k),
        ph: parseFloat(advancedForm.ph),
        temperature: parseFloat(advancedForm.temperature),
        humidity: parseFloat(advancedForm.humidity),
        rainfall: parseFloat(advancedForm.rainfall),
      }
    }

    const soilObj = SOIL_TYPES.find(s => s.id === selectedSoil) || SOIL_TYPES[0]
    const symptomObj = LEAF_SYMPTOMS.find(l => l.id === selectedSymptom) || LEAF_SYMPTOMS[0]
    const seasonObj = SEASONS.find(s => s.id === selectedSeason) || SEASONS[0]

    return {
      crop: selectedCrop,
      days_since_planting: parseInt(daysPlanted),
      soil_n: Math.round(soilObj.n * symptomObj.nMult),
      soil_p: Math.round(soilObj.p * symptomObj.pMult),
      soil_k: Math.round(soilObj.k * symptomObj.kMult),
      ph: soilObj.ph,
      temperature: seasonObj.temp,
      humidity: seasonObj.humidity,
      rainfall: seasonObj.rainfall,
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setResult(null)
    try {
      const payload = getPayload()
      const res = await api.post('/predict', payload)
      setResult(res.data)
      toast.success('Recommendation calculated')
      setTimeout(() => {
        document.getElementById('result-section')?.scrollIntoView({ behavior: 'smooth' })
      }, 100)
    } catch (err) {
      const msg = err.response?.data?.detail || 'Analysis failed. Please check inputs.'
      toast.error(msg)
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setResult(null)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const currentPayload = getPayload()

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Header */}
        <div className="mb-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-3 mb-1">
              <div className="bg-emerald-700 text-white p-2.5 rounded-xl">
                <ShoppingBag size={22} />
              </div>
              <div>
                <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">Which Fertilizer Do I Need To Buy?</h1>
                <p className="text-gray-500 text-xs sm:text-sm mt-0.5">Select your crop and field conditions to determine the exact fertilizer type and dosage to purchase.</p>
              </div>
            </div>
          </div>

          {/* Mode Selector */}
          <div className="bg-gray-200/80 p-1 rounded-xl flex items-center gap-1 self-start sm:self-auto shrink-0">
            <button
              type="button"
              onClick={() => setMode('simple')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-xs font-semibold transition-all ${
                mode === 'simple'
                  ? 'bg-white text-emerald-800 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <Sprout size={14} className="text-emerald-600" />
              Farmer Mode
            </button>
            <button
              type="button"
              onClick={() => setMode('advanced')}
              className={`flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-xs font-semibold transition-all ${
                mode === 'advanced'
                  ? 'bg-white text-emerald-800 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <Sliders size={14} />
              Soil Lab Card
            </button>
          </div>
        </div>

        {/* Main Form */}
        <div className="card shadow-sm border border-gray-100">
          <form onSubmit={handleSubmit} className="space-y-6">
            
            {/* Step 1 & 2: Crop & Planting Days */}
            <div className="bg-emerald-50/50 p-5 rounded-xl border border-emerald-100/80 grid md:grid-cols-2 gap-4">
              <div>
                <label className="label text-emerald-950 font-semibold text-xs uppercase tracking-wider">
                  1. Select Crop
                </label>
                <select
                  value={selectedCrop}
                  onChange={(e) => setSelectedCrop(e.target.value)}
                  className="input-field bg-white font-semibold text-gray-800"
                >
                  {CROPS.map((c) => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="label text-emerald-950 font-semibold text-xs uppercase tracking-wider">
                  2. Days Since Sowing / Planting
                </label>
                <div className="relative">
                  <input
                    type="number"
                    min={0}
                    max={365}
                    value={daysPlanted}
                    onChange={(e) => setDaysPlanted(e.target.value)}
                    className="input-field bg-white font-semibold text-gray-800 pr-16"
                    required
                  />
                  <span className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 text-xs font-semibold">days</span>
                </div>
              </div>
            </div>

            {/* FARMER MODE: Clean visual choices */}
            {mode === 'simple' && (
              <div className="space-y-6 animate-fade-in">
                
                {/* Soil Type */}
                <div>
                  <label className="label text-gray-800 font-semibold text-xs uppercase tracking-wider mb-2">
                    3. Soil Characteristics
                  </label>
                  <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
                    {SOIL_TYPES.map((soil) => (
                      <button
                        key={soil.id}
                        type="button"
                        onClick={() => setSelectedSoil(soil.id)}
                        className={`text-left p-4 rounded-xl border-2 transition-all flex flex-col justify-between ${
                          selectedSoil === soil.id
                            ? 'border-emerald-600 bg-emerald-50/60 shadow-sm'
                            : 'border-gray-100 hover:border-gray-200 bg-white'
                        }`}
                      >
                        <div className="flex items-center justify-between mb-2">
                          <Layers size={18} className={selectedSoil === soil.id ? 'text-emerald-700' : 'text-gray-400'} />
                          {selectedSoil === soil.id && <CheckCircle2 size={16} className="text-emerald-700" />}
                        </div>
                        <div>
                          <p className="font-bold text-gray-900 text-sm">{soil.name}</p>
                          <p className="text-xs text-gray-500 mt-1 leading-relaxed">{soil.desc}</p>
                        </div>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Leaf Symptoms */}
                <div>
                  <label className="label text-gray-800 font-semibold text-xs uppercase tracking-wider mb-2">
                    4. Crop Growth & Leaf Appearance
                  </label>
                  <div className="grid sm:grid-cols-2 gap-3">
                    {LEAF_SYMPTOMS.map((sym) => (
                      <button
                        key={sym.id}
                        type="button"
                        onClick={() => setSelectedSymptom(sym.id)}
                        className={`text-left p-4 rounded-xl border-2 transition-all flex items-start gap-3 ${
                          selectedSymptom === sym.id
                            ? 'border-emerald-600 bg-emerald-50/60 shadow-sm'
                            : 'border-gray-100 hover:border-gray-200 bg-white'
                        }`}
                      >
                        <Activity size={18} className={`mt-0.5 ${selectedSymptom === sym.id ? 'text-emerald-700' : 'text-gray-400'}`} />
                        <div className="flex-1">
                          <div className="flex items-center justify-between">
                            <p className="font-bold text-gray-900 text-sm">{sym.name}</p>
                            {selectedSymptom === sym.id && <CheckCircle2 size={16} className="text-emerald-700" />}
                          </div>
                          <p className="text-xs text-gray-500 mt-1 leading-relaxed">{sym.desc}</p>
                        </div>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Season */}
                <div>
                  <label className="label text-gray-800 font-semibold text-xs uppercase tracking-wider mb-2">
                    5. Current Weather / Season
                  </label>
                  <div className="grid sm:grid-cols-3 gap-3">
                    {SEASONS.map((s) => (
                      <button
                        key={s.id}
                        type="button"
                        onClick={() => setSelectedSeason(s.id)}
                        className={`text-left p-3.5 rounded-xl border-2 transition-all flex items-center gap-3 ${
                          selectedSeason === s.id
                            ? 'border-emerald-600 bg-emerald-50/60 shadow-sm'
                            : 'border-gray-100 hover:border-gray-200 bg-white'
                        }`}
                      >
                        {s.icon}
                        <span className="font-semibold text-gray-900 text-xs">{s.name}</span>
                      </button>
                    ))}
                  </div>
                </div>

                {/* Summary Banner */}
                <div className="bg-gray-100/80 border border-gray-200 rounded-xl p-3.5 text-xs text-gray-600 flex items-center justify-between">
                  <span>
                    <strong>Estimated NPK & pH:</strong> N={currentPayload.soil_n} kg/ha, P={currentPayload.soil_p} kg/ha, K={currentPayload.soil_k} kg/ha, pH={currentPayload.ph}
                  </span>
                  <button
                    type="button"
                    onClick={() => setMode('advanced')}
                    className="text-emerald-700 font-semibold underline hover:text-emerald-900 shrink-0 ml-2"
                  >
                    Adjust Numerically
                  </button>
                </div>

              </div>
            )}

            {/* ADVANCED MODE: Soil Lab Card */}
            {mode === 'advanced' && (
              <div className="space-y-4 animate-fade-in border-t border-gray-100 pt-4">
                <div className="bg-emerald-50 border border-emerald-100 rounded-xl p-3 text-xs text-emerald-800">
                  Enter exact numerical values from an official Soil Testing Laboratory card.
                </div>

                <div className="grid md:grid-cols-3 gap-4">
                  <div>
                    <label className="label">Soil Nitrogen (N)</label>
                    <input
                      type="number"
                      value={advancedForm.soil_n}
                      onChange={(e) => setAdvancedForm({ ...advancedForm, soil_n: e.target.value })}
                      className="input-field"
                      min={0} max={140}
                      required
                    />
                    <span className="text-[10px] text-gray-400">kg/ha (0–140)</span>
                  </div>

                  <div>
                    <label className="label">Soil Phosphorous (P)</label>
                    <input
                      type="number"
                      value={advancedForm.soil_p}
                      onChange={(e) => setAdvancedForm({ ...advancedForm, soil_p: e.target.value })}
                      className="input-field"
                      min={0} max={145}
                      required
                    />
                    <span className="text-[10px] text-gray-400">kg/ha (0–145)</span>
                  </div>

                  <div>
                    <label className="label">Soil Potassium (K)</label>
                    <input
                      type="number"
                      value={advancedForm.soil_k}
                      onChange={(e) => setAdvancedForm({ ...advancedForm, soil_k: e.target.value })}
                      className="input-field"
                      min={0} max={205}
                      required
                    />
                    <span className="text-[10px] text-gray-400">kg/ha (0–205)</span>
                  </div>
                </div>

                <div className="grid md:grid-cols-4 gap-4">
                  <div>
                    <label className="label">Soil pH</label>
                    <input
                      type="number"
                      step={0.1}
                      value={advancedForm.ph}
                      onChange={(e) => setAdvancedForm({ ...advancedForm, ph: e.target.value })}
                      className="input-field"
                      min={0} max={14}
                      required
                    />
                  </div>
                  <div>
                    <label className="label">Temperature (°C)</label>
                    <input
                      type="number"
                      value={advancedForm.temperature}
                      onChange={(e) => setAdvancedForm({ ...advancedForm, temperature: e.target.value })}
                      className="input-field"
                      required
                    />
                  </div>
                  <div>
                    <label className="label">Humidity (%)</label>
                    <input
                      type="number"
                      value={advancedForm.humidity}
                      onChange={(e) => setAdvancedForm({ ...advancedForm, humidity: e.target.value })}
                      className="input-field"
                      required
                    />
                  </div>
                  <div>
                    <label className="label">Rainfall (mm)</label>
                    <input
                      type="number"
                      value={advancedForm.rainfall}
                      onChange={(e) => setAdvancedForm({ ...advancedForm, rainfall: e.target.value })}
                      className="input-field"
                      required
                    />
                  </div>
                </div>
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-emerald-700 hover:bg-emerald-800 text-white font-semibold py-4 rounded-xl transition-all shadow-md flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Loader2 size={18} className="animate-spin" />
                  Calculating Fertilizer to Buy...
                </>
              ) : (
                <>
                  <ShoppingBag size={18} />
                  Calculate Fertilizer to Buy
                </>
              )}
            </button>
          </form>
        </div>

        {/* Result Section */}
        {result && (
          <div id="result-section" className="mt-8 animate-slide-up">
            <PredictionResult result={result} onReset={handleReset} />
          </div>
        )}
      </div>
    </div>
  )
}
