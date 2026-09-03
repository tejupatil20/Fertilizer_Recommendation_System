import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { FlaskConical, History, TrendingUp, Calendar, Download, Loader2, Sprout } from 'lucide-react'
import Navbar from '../components/Navbar'
import { useAuth } from '../context/AuthContext'
import api from '../api/axios'
import toast from 'react-hot-toast'

function StatCard({ icon, label, value, color = 'primary' }) {
  const colors = {
    primary: 'bg-primary-50 text-primary-600',
    amber: 'bg-amber-50 text-amber-600',
    blue: 'bg-blue-50 text-blue-600',
  }
  return (
    <div className="card flex items-center gap-4">
      <div className={`p-3 rounded-xl ${colors[color]}`}>{icon}</div>
      <div>
        <p className="text-sm text-gray-500">{label}</p>
        <p className="text-2xl font-bold text-gray-900 mt-0.5">{value}</p>
      </div>
    </div>
  )
}

export default function Dashboard() {
  const { user } = useAuth()
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await api.get('/predict/history?limit=5')
        setHistory(res.data)
      } catch (err) {
        toast.error('Failed to load prediction history')
      } finally {
        setLoading(false)
      }
    }
    fetchHistory()
  }, [])

  const totalPredictions = history.length
  const mostUsed = history.length > 0
    ? history.reduce((acc, p) => {
        acc[p.predicted_fertilizer] = (acc[p.predicted_fertilizer] || 0) + 1
        return acc
      }, {})
    : {}
  const topFertilizer = Object.keys(mostUsed).sort((a, b) => mostUsed[b] - mostUsed[a])[0] || '—'
  const lastDate = history.length > 0
    ? new Date(history[0].created_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
    : 'Never'

  const handleDownload = async (id) => {
    try {
      const res = await api.get(`/reports/${id}/download`, { responseType: 'blob' })
      const url = window.URL.createObjectURL(new Blob([res.data], { type: 'application/pdf' }))
      const a = document.createElement('a')
      a.href = url
      a.download = `fertilizer_report_${id}.pdf`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (err) {
      toast.error('Failed to download report')
    }
  }

  const confidenceColor = (score) => {
    if (score >= 80) return 'text-primary-700 bg-primary-100'
    if (score >= 60) return 'text-amber-700 bg-amber-100'
    return 'text-red-700 bg-red-100'
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Good day, <span className="text-primary-600">{user?.username?.split(' ')[0]}</span>! 👋
          </h1>
          <p className="text-gray-500 mt-1">Here's an overview of your fertilizer recommendations.</p>
        </div>

        {/* Stats */}
        <div className="grid sm:grid-cols-3 gap-4 mb-8">
          <StatCard icon={<History size={22} />} label="Recent Predictions" value={loading ? '...' : totalPredictions} color="primary" />
          <StatCard icon={<Sprout size={22} />} label="Most Used Fertilizer" value={loading ? '...' : topFertilizer} color="amber" />
          <StatCard icon={<Calendar size={22} />} label="Last Analysis" value={loading ? '...' : lastDate} color="blue" />
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Quick Action */}
          <div className="lg:col-span-1">
            <div className="card h-full flex flex-col items-center justify-center text-center py-10 border-2 border-dashed border-primary-200 hover:border-primary-400 transition-colors group cursor-pointer">
              <div className="bg-primary-100 text-primary-600 p-5 rounded-2xl mb-5 group-hover:scale-110 transition-transform">
                <FlaskConical size={36} />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">Get New Recommendation</h3>
              <p className="text-gray-500 text-sm mb-6">Enter your soil data to receive an AI-powered fertilizer recommendation.</p>
              <Link to="/predict" className="btn-primary">
                Start Analysis
              </Link>
            </div>
          </div>

          {/* Recent Predictions */}
          <div className="lg:col-span-2 card">
            <div className="flex justify-between items-center mb-5">
              <h2 className="text-lg font-bold text-gray-900">Recent Predictions</h2>
              <Link to="/history" className="text-sm text-primary-600 font-medium hover:underline flex items-center gap-1">
                View All <History size={14} />
              </Link>
            </div>

            {loading ? (
              <div className="space-y-3">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="skeleton h-14 w-full rounded-lg" />
                ))}
              </div>
            ) : history.length === 0 ? (
              <div className="text-center py-12">
                <FlaskConical size={40} className="text-gray-300 mx-auto mb-3" />
                <p className="text-gray-400 font-medium">No predictions yet</p>
                <p className="text-gray-400 text-sm mt-1">Start by getting your first recommendation</p>
                <Link to="/predict" className="mt-4 inline-block btn-primary text-sm">
                  Get Started
                </Link>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="text-left border-b border-gray-100">
                      <th className="pb-3 text-gray-500 font-medium">Crop</th>
                      <th className="pb-3 text-gray-500 font-medium">Fertilizer</th>
                      <th className="pb-3 text-gray-500 font-medium">Confidence</th>
                      <th className="pb-3 text-gray-500 font-medium">Stage</th>
                      <th className="pb-3 text-gray-500 font-medium">Date</th>
                      <th className="pb-3 text-gray-500 font-medium">PDF</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-50">
                    {history.map((p) => (
                      <tr key={p.id} className="hover:bg-gray-50 transition-colors">
                        <td className="py-3 font-medium text-gray-800 capitalize">{p.crop}</td>
                        <td className="py-3">
                          <span className="badge-green">{p.predicted_fertilizer}</span>
                        </td>
                        <td className="py-3">
                          <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${confidenceColor(p.confidence_score)}`}>
                            {p.confidence_score.toFixed(1)}%
                          </span>
                        </td>
                        <td className="py-3 text-gray-500 text-xs max-w-[120px] truncate">{p.growth_stage || '—'}</td>
                        <td className="py-3 text-gray-400 text-xs whitespace-nowrap">
                          {new Date(p.created_at).toLocaleDateString('en-IN')}
                        </td>
                        <td className="py-3">
                          <button
                            onClick={() => handleDownload(p.id)}
                            className="text-primary-600 hover:text-primary-800 hover:bg-primary-50 p-1.5 rounded-lg transition-all"
                            title="Download PDF"
                          >
                            <Download size={16} />
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
