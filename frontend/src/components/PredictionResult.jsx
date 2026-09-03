import { Download, RefreshCw, Leaf, CheckCircle2, ShoppingBag, Scale, Sparkles, FileText } from 'lucide-react'
import api from '../api/axios'
import toast from 'react-hot-toast'

function ConfidenceBar({ score }) {
  let barColor = 'bg-emerald-600'
  let textColor = 'text-emerald-800'
  let bgColor = 'bg-emerald-50'
  let label = 'High Confidence Match'

  if (score < 60) {
    barColor = 'bg-amber-500'; textColor = 'text-amber-800'; bgColor = 'bg-amber-50'; label = 'Moderate Confidence'
  } else if (score < 80) {
    barColor = 'bg-emerald-500'; textColor = 'text-emerald-700'; bgColor = 'bg-emerald-50'; label = 'Good Match'
  }

  return (
    <div className={`p-4 rounded-xl ${bgColor} border border-emerald-100`}>
      <div className="flex justify-between items-center mb-2">
        <span className={`text-xs font-bold uppercase tracking-wider ${textColor}`}>{label}</span>
        <span className={`text-base font-bold ${textColor}`}>{score.toFixed(1)}%</span>
      </div>
      <div className="h-2.5 bg-white rounded-full overflow-hidden shadow-inner">
        <div
          className={`h-full ${barColor} rounded-full transition-all duration-700`}
          style={{ width: `${Math.min(score, 100)}%` }}
        />
      </div>
    </div>
  )
}

export default function PredictionResult({ result, onReset }) {
  const handleDownload = async () => {
    try {
      const res = await api.get(`/reports/${result.id}/download`, { responseType: 'blob' })
      const url = window.URL.createObjectURL(new Blob([res.data], { type: 'application/pdf' }))
      const a = document.createElement('a')
      a.href = url
      a.download = `fertilizer_recommendation_${result.id}_${result.crop.toLowerCase()}.pdf`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
      toast.success('PDF advisory report downloaded')
    } catch (err) {
      toast.error('Failed to download PDF report')
    }
  }

  const dosageVal = result.dosage_kg_per_acre || 40

  return (
    <div className="space-y-6">
      
      {/* Hero Recommendation Card: FERTILIZER TO BUY */}
      <div className="bg-white rounded-2xl border-2 border-emerald-600 shadow-xl overflow-hidden">
        <div className="bg-emerald-700 px-6 py-3 text-white flex items-center justify-between">
          <div className="flex items-center gap-2">
            <ShoppingBag size={18} className="text-emerald-200" />
            <span className="text-xs font-bold uppercase tracking-wider">Recommended Purchase</span>
          </div>
          <span className="text-xs bg-emerald-800 text-emerald-100 px-3 py-1 rounded-full font-medium">
            Analysis #{result.id}
          </span>
        </div>

        <div className="p-8 text-center bg-gradient-to-b from-emerald-50/50 to-white">
          <p className="text-xs font-bold uppercase tracking-widest text-emerald-800 mb-2">
            Fertilizer to Buy for Your Crop ({result.crop})
          </p>
          <h1 className="text-4xl sm:text-5xl font-black text-gray-900 tracking-tight my-2">
            {result.predicted_fertilizer}
          </h1>

          {/* Dosage & Purchase Quantity Callout */}
          <div className="mt-5 inline-flex flex-col sm:flex-row items-center gap-3 bg-white px-6 py-3 rounded-2xl border border-emerald-200 shadow-sm">
            <div className="flex items-center gap-2 text-emerald-800 font-bold text-sm">
              <Scale size={18} className="text-emerald-600" />
              <span>Purchase Dosage: {dosageVal} kg per acre</span>
            </div>
            <span className="hidden sm:inline text-gray-300">|</span>
            <span className="text-xs text-gray-500 font-medium">
              Approx. {Math.ceil(dosageVal / 45)} Bag ({dosageVal <= 45 ? '45 kg' : '50 kg'} standard bag per acre)
            </span>
          </div>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Growth Stage & Confidence Details */}
        <div className="card space-y-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-gray-500">Crop Growth Context</h3>
          
          {result.growth_stage && (
            <div className="flex items-center gap-3 bg-emerald-50/80 p-4 rounded-xl border border-emerald-100">
              <div className="p-2.5 bg-emerald-600 text-white rounded-lg">
                <Leaf size={20} />
              </div>
              <div>
                <p className="text-xs text-emerald-700 font-medium">Detected Stage</p>
                <p className="font-bold text-emerald-950 text-base">{result.growth_stage}</p>
              </div>
            </div>
          )}

          <ConfidenceBar score={result.confidence_score} />
        </div>

        {/* Input Summary */}
        <div className="card">
          <h3 className="text-xs font-bold uppercase tracking-wider text-gray-500 mb-4">Analysis Input Summary</h3>
          <div className="grid grid-cols-2 gap-2.5 text-xs">
            {[
              { label: 'Crop', value: result.crop },
              { label: 'Days Planted', value: `${result.days_since_planting} days` },
              { label: 'Nitrogen (N)', value: `${result.soil_n} kg/ha` },
              { label: 'Phosphorous (P)', value: `${result.soil_p} kg/ha` },
              { label: 'Potassium (K)', value: `${result.soil_k} kg/ha` },
              { label: 'Soil pH', value: result.ph },
              { label: 'Temperature', value: `${result.temperature}°C` },
              { label: 'Humidity', value: `${result.humidity}%` },
            ].map((item) => (
              <div key={item.label} className="bg-gray-50/80 rounded-lg p-2.5 border border-gray-100">
                <p className="text-gray-400 font-medium">{item.label}</p>
                <p className="font-semibold text-gray-800 mt-0.5">{item.value}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* AI Explanation / Agronomist Notes */}
      {result.gemini_explanation && (
        <div className="card border-l-4 border-emerald-600 space-y-3">
          <div className="flex items-center gap-2">
            <Sparkles size={18} className="text-emerald-600" />
            <h3 className="font-bold text-gray-900 text-sm">Agronomic Advice & Explanation</h3>
          </div>
          <p className="text-gray-700 text-sm leading-relaxed bg-gray-50 p-4 rounded-xl border border-gray-100">
            {result.gemini_explanation}
          </p>

          <div className="grid sm:grid-cols-2 gap-4 pt-2">
            {result.application_method && (
              <div className="bg-emerald-50/60 rounded-xl p-3.5 border border-emerald-100">
                <p className="text-xs font-bold text-emerald-800 uppercase tracking-wider mb-1">Application Method</p>
                <p className="text-xs text-gray-700 leading-normal">{result.application_method}</p>
              </div>
            )}
            {result.timing_advice && (
              <div className="bg-emerald-50/60 rounded-xl p-3.5 border border-emerald-100">
                <p className="text-xs font-bold text-emerald-800 uppercase tracking-wider mb-1">Timing & Weather Advice</p>
                <p className="text-xs text-gray-700 leading-normal">{result.timing_advice}</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Alternative Options */}
      {result.alternatives && result.alternatives.length > 0 && (
        <div className="card">
          <h3 className="text-xs font-bold uppercase tracking-wider text-gray-500 mb-3">Alternative Substitute Fertilizers</h3>
          <div className="flex flex-wrap gap-2">
            {result.alternatives.map((alt) => (
              <span key={alt} className="bg-gray-100 text-gray-800 font-semibold px-4 py-2 rounded-xl text-xs border border-gray-200">
                {alt}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="flex flex-col sm:flex-row gap-3 pt-2">
        <button
          onClick={handleDownload}
          className="flex-1 flex items-center justify-center gap-2 bg-emerald-700 hover:bg-emerald-800 text-white font-semibold py-4 px-6 rounded-xl transition-all shadow-md"
        >
          <Download size={18} />
          Download Printable PDF Advisory Report
        </button>
        <button
          onClick={onReset}
          className="flex-1 flex items-center justify-center gap-2 bg-white hover:bg-gray-50 text-gray-700 font-semibold py-4 px-6 rounded-xl border border-gray-200 transition-all"
        >
          <RefreshCw size={18} />
          New Advisory Calculation
        </button>
      </div>
    </div>
  )
}
