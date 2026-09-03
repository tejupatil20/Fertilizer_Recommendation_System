import { useState, useEffect } from 'react'
import Navbar from '../../components/Navbar'
import api from '../../api/axios'
import toast from 'react-hot-toast'
import { Activity, RefreshCw, Loader2, CheckCircle, AlertTriangle } from 'lucide-react'

export default function ModelMetrics() {
  const [metrics, setMetrics] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchMetrics = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await api.get('/admin/model-metrics')
      if (res.data.error) {
        setError(res.data.error)
      } else {
        setMetrics(res.data)
      }
    } catch {
      setError('Failed to load model metrics. Ensure the server is running.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchMetrics() }, [])

  const report = metrics?.report || {}
  const classNames = metrics?.class_names || []

  // Extract macro avg
  const macroAvg = report['macro avg'] || {}
  const weightedAvg = report['weighted avg'] || {}

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <div className="flex items-center gap-3 mb-1">
              <div className="bg-primary-600 text-white p-2 rounded-xl"><Activity size={20} /></div>
              <h1 className="text-2xl font-bold text-gray-900">Model Performance Metrics</h1>
            </div>
            <p className="text-gray-500 text-sm ml-11">RandomForest Classifier — Evaluation Results</p>
          </div>
          <button onClick={fetchMetrics} disabled={loading} className="btn-secondary flex items-center gap-2 text-sm">
            {loading ? <Loader2 size={16} className="animate-spin" /> : <RefreshCw size={16} />}
            Refresh
          </button>
        </div>

        {loading ? (
          <div className="space-y-4">
            <div className="skeleton h-32 rounded-xl" />
            <div className="skeleton h-64 rounded-xl" />
            <div className="skeleton h-96 rounded-xl" />
          </div>
        ) : error ? (
          <div className="card text-center py-16">
            <AlertTriangle size={48} className="mx-auto text-amber-400 mb-4" />
            <p className="font-semibold text-gray-800 text-lg mb-2">Metrics Not Available</p>
            <p className="text-gray-500 text-sm max-w-md mx-auto mb-4">{error}</p>
            <div className="bg-gray-50 rounded-xl p-4 text-left text-sm font-mono text-gray-600 max-w-md mx-auto">
              cd backend<br />
              python ml/train_model.py
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            {/* Summary cards */}
            <div className="grid sm:grid-cols-4 gap-4">
              {[
                { label: 'Overall Accuracy', value: `${(metrics.accuracy * 100).toFixed(2)}%`, icon: <CheckCircle size={20} />, color: 'text-primary-600 bg-primary-50' },
                { label: 'Macro Precision', value: `${((macroAvg.precision || 0) * 100).toFixed(2)}%`, icon: <Activity size={20} />, color: 'text-blue-600 bg-blue-50' },
                { label: 'Macro Recall', value: `${((macroAvg.recall || 0) * 100).toFixed(2)}%`, icon: <Activity size={20} />, color: 'text-purple-600 bg-purple-50' },
                { label: 'Macro F1-Score', value: `${((macroAvg['f1-score'] || 0) * 100).toFixed(2)}%`, icon: <Activity size={20} />, color: 'text-amber-600 bg-amber-50' },
              ].map((m) => (
                <div key={m.label} className="card text-center">
                  <div className={`w-12 h-12 rounded-xl flex items-center justify-center mx-auto mb-3 ${m.color}`}>
                    {m.icon}
                  </div>
                  <p className="text-2xl font-black text-gray-900">{m.value}</p>
                  <p className="text-xs text-gray-500 mt-1">{m.label}</p>
                </div>
              ))}
            </div>

            {/* Confusion Matrix */}
            {metrics.confusion_matrix_b64 && (
              <div className="card">
                <h2 className="font-bold text-gray-800 mb-4">Confusion Matrix</h2>
                <div className="flex justify-center">
                  <img
                    src={`data:image/png;base64,${metrics.confusion_matrix_b64}`}
                    alt="Confusion Matrix"
                    className="max-w-full rounded-xl border border-gray-100 shadow-sm"
                    style={{ maxHeight: '500px' }}
                  />
                </div>
              </div>
            )}

            {/* Per-class classification report */}
            <div className="card">
              <h2 className="font-bold text-gray-800 mb-4">Per-Class Classification Report</h2>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="bg-gray-50">
                    <tr>
                      {['Fertilizer', 'Precision', 'Recall', 'F1-Score', 'Support'].map((h) => (
                        <th key={h} className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">{h}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-50">
                    {classNames.map((cls) => {
                      const r = report[cls] || {}
                      return (
                        <tr key={cls} className="hover:bg-gray-50">
                          <td className="px-4 py-3 font-medium text-gray-800">{cls}</td>
                          <td className="px-4 py-3 text-gray-600">{((r.precision || 0) * 100).toFixed(1)}%</td>
                          <td className="px-4 py-3 text-gray-600">{((r.recall || 0) * 100).toFixed(1)}%</td>
                          <td className="px-4 py-3">
                            <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${
                              (r['f1-score'] || 0) >= 0.8
                                ? 'bg-primary-100 text-primary-700'
                                : (r['f1-score'] || 0) >= 0.6
                                ? 'bg-amber-100 text-amber-700'
                                : 'bg-red-100 text-red-700'
                            }`}>
                              {((r['f1-score'] || 0) * 100).toFixed(1)}%
                            </span>
                          </td>
                          <td className="px-4 py-3 text-gray-400 font-mono">{Math.round(r.support || 0)}</td>
                        </tr>
                      )
                    })}
                  </tbody>
                  <tfoot className="bg-primary-50">
                    <tr>
                      <td className="px-4 py-3 font-bold text-primary-800">Weighted Avg</td>
                      <td className="px-4 py-3 font-semibold text-primary-700">{((weightedAvg.precision || 0) * 100).toFixed(1)}%</td>
                      <td className="px-4 py-3 font-semibold text-primary-700">{((weightedAvg.recall || 0) * 100).toFixed(1)}%</td>
                      <td className="px-4 py-3 font-semibold text-primary-700">{((weightedAvg['f1-score'] || 0) * 100).toFixed(1)}%</td>
                      <td className="px-4 py-3 font-semibold text-primary-700 font-mono">5000</td>
                    </tr>
                  </tfoot>
                </table>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
