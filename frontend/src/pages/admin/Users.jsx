import { useState, useEffect } from 'react'
import Navbar from '../../components/Navbar'
import api from '../../api/axios'
import toast from 'react-hot-toast'
import { Users, Search, User, ShieldCheck, Calendar } from 'lucide-react'

export default function AdminUsers() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')

  useEffect(() => {
    const fetch = async () => {
      try {
        const res = await api.get('/admin/users')
        setUsers(res.data)
      } catch {
        toast.error('Failed to load users')
      } finally {
        setLoading(false)
      }
    }
    fetch()
  }, [])

  const filtered = users.filter((u) =>
    u.username.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
          <div>
            <div className="flex items-center gap-3 mb-1">
              <div className="bg-primary-600 text-white p-2 rounded-xl">
                <Users size={20} />
              </div>
              <h1 className="text-2xl font-bold text-gray-900">Registered Users</h1>
            </div>
            <p className="text-gray-500 text-sm ml-11">{users.length} total users</p>
          </div>
          <div className="relative">
            <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              placeholder="Search by username..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="input-field pl-9 w-64"
            />
          </div>
        </div>

        <div className="card overflow-hidden p-0">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 border-b border-gray-100">
                <tr>
                  {['#', 'Username', 'Role', 'Joined Date'].map((h) => (
                    <th key={h} className="px-5 py-4 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {loading ? (
                  [...Array(5)].map((_, i) => (
                    <tr key={i}>
                      {[...Array(4)].map((_, j) => (
                        <td key={j} className="px-5 py-4"><div className="skeleton h-5 w-24 rounded" /></td>
                      ))}
                    </tr>
                  ))
                ) : filtered.length === 0 ? (
                  <tr>
                    <td colSpan={4} className="text-center py-16 text-gray-400">
                      <Users size={36} className="mx-auto mb-3 text-gray-200" />
                      <p>No users found</p>
                    </td>
                  </tr>
                ) : (
                  filtered.map((u, idx) => (
                    <tr key={u.id} className="hover:bg-gray-50">
                      <td className="px-5 py-4 text-gray-400 text-xs">{idx + 1}</td>
                      <td className="px-5 py-4">
                        <div className="flex items-center gap-3">
                          <div className="w-8 h-8 bg-primary-600 text-white rounded-full flex items-center justify-center text-xs font-bold">
                            {u.username[0].toUpperCase()}
                          </div>
                          <span className="font-medium text-gray-800">{u.username}</span>
                        </div>
                      </td>
                      <td className="px-5 py-4">
                        {u.role === 'admin' ? (
                          <span className="badge-blue flex items-center gap-1 w-fit">
                            <ShieldCheck size={12} /> Admin
                          </span>
                        ) : (
                          <span className="badge-green flex items-center gap-1 w-fit">
                            <User size={12} /> Farmer
                          </span>
                        )}
                      </td>
                      <td className="px-5 py-4 text-gray-400 text-xs flex items-center gap-1.5 mt-2">
                        <Calendar size={12} />
                        {u.created_at ? new Date(u.created_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }) : '—'}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  )
}
