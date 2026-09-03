import { useState, useEffect } from 'react'
import Navbar from '../../components/Navbar'
import FertilizerChart from '../../components/charts/FertilizerChart'
import CropQueryChart from '../../components/charts/CropQueryChart'
import api from '../../api/axios'
import toast from 'react-hot-toast'
import {
  BarChart2, Users, FlaskConical, Sprout,
  TrendingUp, RefreshCw, Loader2,
} from 'lucide-react'
import {
  ResponsiveContainer, LineChart, Line, XAxis, YAxis,
  CartesianGrid, Tooltip
} from 'recharts'

function StatCard({ icon, label, value, sub, color = 'primary' }) {
  const colors = {
    primary: 'bg-primary-50 text-primary-600',
    blue: 'bg-blue-50 text-blue-600',
    amber: 'bg-amber-50 text-amber-600',
    purple: 'bg-purple-50 text-purple-600',
  }
  return (
    <div className="card flex items-center gap-4">
      <div className={`p-3 rounded-xl ${colors[color]}`}>{icon}</div>
      <div>
        <p className="text-sm text-gray-500">{label}</p>
        <p className="text-2xl font-bold text-gray-900">{value}</p>
        {sub && <p className="text-xs text-gray-400 mt-0.5">{sub}</p>}
      </div>
    </div>
  )
}

export default function AdminDashboard() {
  const [analytics, setAnalytics] = useState(null)
  const [loading, setLoading] = useState(true)

  const fetchAnalytics = async () => {
    setLoading(true)
    try {
      const res = await api.get('/admin/analytics')
      setAnalytics(res.data)
    } catch {
      toast.error('Failed to load analytics')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchAnalytics() }, [])

  const topFertilizer = analytics?.most_recommended?.[0]?.fertilizer || '—'
  const topCrop = analytics?.most_queried_crop?.[0]?.crop || '—'

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
            <p className="text-gray-500 mt-1">System analytics and insights</p>
          </div>
          <button
            onClick={fetchAnalytics}
            disabled={loading}
            className="flex items-center gap-2 btn-secondary text-sm"
          >
            {loading ? <Loader2 size={16} className="animate-spin" /> : <RefreshCw size={16} />}
            Refresh
          </button>
        </div>

        {/* Stats row */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <StatCard icon={<FlaskConical size={22} />} label="Total Predictions" value={loading ? '...' : analytics?.total_predictions ?? 0} color="primary" />
          <StatCard icon={<Users size={22} />} label="Registered Users" value={loading ? '...' : analytics?.total_users ?? 0} color="blue" />
          <StatCard icon={<Sprout size={22} />} label="Top Fertilizer" value={loading ? '...' : topFertilizer} sub="Most recommended" color="amber" />
          <StatCard icon={<TrendingUp size={22} />} label="Top Crop" value={loading ? '...' : topCrop} sub="Most analyzed" color="purple" />
        </div>

        {/* Charts row */}
        <div className="grid lg:grid-cols-2 gap-6 mb-6">
          {/* Fertilizer bar chart */}
          <div className="card">
            <h2 className="font-bold text-gray-800 mb-4 flex items-center gap-2">
              <BarChart2 size={18} className="text-primary-600" />
              Fertilizer Usage Distribution
            </h2>
            {loading ? (
              <div className="skeleton h-64 rounded-xl" />
            ) : analytics?.most_recommended?.length > 0 ? (
              <FertilizerChart data={analytics.most_recommended} />
            ) : (
              <div className="h-64 flex items-center justify-center text-gray-400 text-sm">No data yet</div>
            )}
          </div>

          {/* Crop pie chart */}
          <div className="card">
            <h2 className="font-bold text-gray-800 mb-4 flex items-center gap-2">
              <Sprout size={18} className="text-primary-600" />
              Crop Query Distribution
            </h2>
            {loading ? (
              <div className="skeleton h-64 rounded-xl" />
            ) : analytics?.most_queried_crop?.length > 0 ? (
              <CropQueryChart data={analytics.most_queried_crop} />
            ) : (
              <div className="h-64 flex items-center justify-center text-gray-400 text-sm">No data yet</div>
            )}
          </div>
        </div>

        {/* Predictions over time */}
        <div className="card">
          <h2 className="font-bold text-gray-800 mb-4 flex items-center gap-2">
            <TrendingUp size={18} className="text-primary-600" />
            Predictions Over Time (Last 30 Days)
          </h2>
          {loading ? (
            <div className="skeleton h-56 rounded-xl" />
          ) : analytics?.predictions_over_time?.length > 0 ? (
            <ResponsiveContainer width="100%" height={220}>
              <LineChart data={analytics.predictions_over_time.map((d) => ({ date: d.date?.slice(5), count: d.count }))}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="date" tick={{ fontSize: 11, fill: '#6b7280' }} />
                <YAxis tick={{ fontSize: 11, fill: '#6b7280' }} />
                <Tooltip contentStyle={{ borderRadius: '8px', fontSize: 12 }} />
                <Line type="monotone" dataKey="count" stroke="#16a34a" strokeWidth={2.5} dot={{ fill: '#16a34a', r: 4 }} name="Predictions" />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-56 flex items-center justify-center text-gray-400 text-sm">
              No prediction data for the last 30 days
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
