import { useState, useEffect, useCallback } from 'react'
import Navbar from '../../components/Navbar'
import api from '../../api/axios'
import toast from 'react-hot-toast'
import { History, Download, ChevronLeft, ChevronRight, Filter } from 'lucide-react'

const CROPS = ['All', 'Maize', 'Sugarcane', 'Cotton', 'Paddy', 'Wheat', 'Rice', 'Barley', 'Millets', 'Tobacco']

const confidenceColor = (score) => {
  if (score >= 80) return 'text-primary-700 bg-primary-100'
  if (score >= 60) return 'text-amber-700 bg-amber-100'
  return 'text-red-700 bg-red-100'
}

export default function AdminPredictions() {
  const [records, setRecords] = useState([])
  const [loading, setLoading] = useState(true)
  const [cropFilter, setCropFilter] = useState('All')
  const [page, setPage] = useState(0)
  const limit = 15

  const fetch = useCallback(async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams({ limit, offset: page * limit })
      if (cropFilter !== 'All') params.set('crop', cropFilter)
      const res = await api.get(`/admin/predictions?${params}`)
      setRecords(res.data)
    } catch {
      toast.error('Failed to load predictions')
    } finally {
      setLoading(false)
    }
  }, [page, cropFilter])

  useEffect(() => { fetch() }, [fetch])

  const handleDownload = async (id, crop) => {
    try {
      const res = await api.get(`/reports/${id}/download`, { responseType: 'blob' })
      const url = window.URL.createObjectURL(new Blob([res.data], { type: 'application/pdf' }))
      const a = document.createElement('a')
      a.href = url
      a.download = `report_${id}_${crop}.pdf`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch {
      toast.error('Download failed')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
          <div>
            <div className="flex items-center gap-3 mb-1">
              <div className="bg-primary-600 text-white p-2 rounded-xl">
                <History size={20} />
              </div>
              <h1 className="text-2xl font-bold text-gray-900">All Predictions</h1>
            </div>
            <p className="text-gray-500 text-sm ml-11">All farmer prediction records</p>
          </div>
          <div className="flex items-center gap-2">
            <Filter size={16} className="text-gray-400" />
            <select
              value={cropFilter}
              onChange={(e) => { setCropFilter(e.target.value); setPage(0) }}
              className="input-field py-2 w-auto"
            >
              {CROPS.map((c) => <option key={c}>{c}</option>)}
            </select>
          </div>
        </div>

        <div className="card overflow-hidden p-0">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 border-b border-gray-100">
                <tr>
                  {['#', 'Crop', 'Fertilizer', 'Confidence', 'Growth Stage', 'Date', 'Report'].map((h) => (
                    <th key={h} className="px-4 py-3.5 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {loading ? (
                  [...Array(5)].map((_, i) => (
                    <tr key={i}>{[...Array(7)].map((_, j) => <td key={j} className="px-4 py-3"><div className="skeleton h-5 rounded" /></td>)}</tr>
                  ))
                ) : records.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="text-center py-12 text-gray-400">No records found</td>
                  </tr>
                ) : (
                  records.map((r, idx) => (
                    <tr key={r.id} className="hover:bg-gray-50">
                      <td className="px-4 py-3 text-gray-400 text-xs">{page * limit + idx + 1}</td>
                      <td className="px-4 py-3 font-medium capitalize">{r.crop}</td>
                      <td className="px-4 py-3"><span className="badge-green">{r.predicted_fertilizer}</span></td>
                      <td className="px-4 py-3">
                        <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${confidenceColor(r.confidence_score)}`}>
                          {r.confidence_score.toFixed(1)}%
                        </span>
                      </td>
                      <td className="px-4 py-3 text-gray-500 text-xs max-w-[130px] truncate">{r.growth_stage || '—'}</td>
                      <td className="px-4 py-3 text-gray-400 text-xs whitespace-nowrap">
                        {new Date(r.created_at).toLocaleDateString('en-IN')}
                      </td>
                      <td className="px-4 py-3">
                        <button
                          onClick={() => handleDownload(r.id, r.crop)}
                          className="text-primary-600 hover:bg-primary-50 p-1.5 rounded-lg transition-all"
                        >
                          <Download size={15} />
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
          <div className="flex items-center justify-between px-4 py-3 border-t border-gray-100">
            <p className="text-sm text-gray-500">{records.length} records</p>
            <div className="flex items-center gap-2">
              <button onClick={() => setPage(Math.max(0, page - 1))} disabled={page === 0} className="p-2 rounded-lg border border-gray-200 disabled:opacity-40 hover:bg-gray-50">
                <ChevronLeft size={16} />
              </button>
              <span className="text-sm font-medium">Page {page + 1}</span>
              <button onClick={() => setPage(page + 1)} disabled={records.length < limit} className="p-2 rounded-lg border border-gray-200 disabled:opacity-40 hover:bg-gray-50">
                <ChevronRight size={16} />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
