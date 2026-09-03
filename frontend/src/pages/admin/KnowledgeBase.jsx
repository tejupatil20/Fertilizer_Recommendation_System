import { useState, useEffect } from 'react'
import Navbar from '../../components/Navbar'
import api from '../../api/axios'
import toast from 'react-hot-toast'
import { BookOpen, Plus, Edit2, Trash2, X, Loader2, Save } from 'lucide-react'

const EMPTY_FORM = {
  fertilizer_name: '',
  composition: '',
  best_application_stage: '',
  precautions: '',
  description: '',
}

function Modal({ title, onClose, children }) {
  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center px-6 py-4 border-b border-gray-100">
          <h3 className="font-bold text-gray-900">{title}</h3>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 p-1 rounded-lg hover:bg-gray-100">
            <X size={20} />
          </button>
        </div>
        <div className="px-6 py-5">{children}</div>
      </div>
    </div>
  )
}

export default function KnowledgeBase() {
  const [entries, setEntries] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [editEntry, setEditEntry] = useState(null)
  const [form, setForm] = useState(EMPTY_FORM)
  const [saving, setSaving] = useState(false)
  const [deleteId, setDeleteId] = useState(null)

  const fetchEntries = async () => {
    try {
      const res = await api.get('/admin/knowledge-base')
      setEntries(res.data)
    } catch {
      toast.error('Failed to load knowledge base')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchEntries() }, [])

  const openAdd = () => { setEditEntry(null); setForm(EMPTY_FORM); setShowModal(true) }
  const openEdit = (entry) => { setEditEntry(entry); setForm({ ...entry }); setShowModal(true) }
  const closeModal = () => { setShowModal(false); setEditEntry(null); setForm(EMPTY_FORM) }

  const handleSave = async () => {
    if (!form.fertilizer_name.trim()) { toast.error('Fertilizer name is required'); return }
    setSaving(true)
    try {
      if (editEntry) {
        await api.put(`/admin/knowledge-base/${editEntry.id}`, form)
        toast.success('Entry updated')
      } else {
        await api.post('/admin/knowledge-base', form)
        toast.success('Entry added')
      }
      closeModal()
      fetchEntries()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Save failed')
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = async (id) => {
    try {
      await api.delete(`/admin/knowledge-base/${id}`)
      toast.success('Entry deleted')
      setDeleteId(null)
      fetchEntries()
    } catch {
      toast.error('Delete failed')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <div className="flex items-center gap-3 mb-1">
              <div className="bg-primary-600 text-white p-2 rounded-xl"><BookOpen size={20} /></div>
              <h1 className="text-2xl font-bold text-gray-900">Fertilizer Knowledge Base</h1>
            </div>
            <p className="text-gray-500 text-sm ml-11">{entries.length} entries</p>
          </div>
          <button onClick={openAdd} className="btn-primary flex items-center gap-2">
            <Plus size={16} /> Add Entry
          </button>
        </div>

        {loading ? (
          <div className="space-y-3">{[1, 2, 3].map((i) => <div key={i} className="skeleton h-24 rounded-xl" />)}</div>
        ) : (
          <div className="grid md:grid-cols-2 gap-4">
            {entries.map((entry) => (
              <div key={entry.id} className="card hover:shadow-md transition-shadow">
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <h3 className="font-bold text-gray-900 text-lg">{entry.fertilizer_name}</h3>
                    {entry.composition && (
                      <span className="text-xs text-primary-700 font-medium bg-primary-50 px-2 py-0.5 rounded-full">
                        {entry.composition}
                      </span>
                    )}
                  </div>
                  <div className="flex gap-1">
                    <button onClick={() => openEdit(entry)} className="p-2 text-gray-400 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-all">
                      <Edit2 size={15} />
                    </button>
                    <button onClick={() => setDeleteId(entry.id)} className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all">
                      <Trash2 size={15} />
                    </button>
                  </div>
                </div>
                {entry.best_application_stage && (
                  <p className="text-xs text-gray-500 mb-1">
                    <span className="font-medium">Best Stage:</span> {entry.best_application_stage}
                  </p>
                )}
                {entry.description && (
                  <p className="text-sm text-gray-600 line-clamp-2">{entry.description}</p>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Add/Edit Modal */}
      {showModal && (
        <Modal title={editEntry ? 'Edit Fertilizer Entry' : 'Add New Fertilizer'} onClose={closeModal}>
          <div className="space-y-4">
            {[
              { label: 'Fertilizer Name *', key: 'fertilizer_name', type: 'input' },
              { label: 'Composition', key: 'composition', type: 'input' },
              { label: 'Best Application Stage', key: 'best_application_stage', type: 'input' },
              { label: 'Precautions', key: 'precautions', type: 'textarea' },
              { label: 'Description', key: 'description', type: 'textarea' },
            ].map(({ label, key, type }) => (
              <div key={key}>
                <label className="label">{label}</label>
                {type === 'textarea' ? (
                  <textarea
                    value={form[key]}
                    onChange={(e) => setForm({ ...form, [key]: e.target.value })}
                    rows={3}
                    className="input-field resize-none"
                  />
                ) : (
                  <input
                    type="text"
                    value={form[key]}
                    onChange={(e) => setForm({ ...form, [key]: e.target.value })}
                    className="input-field"
                  />
                )}
              </div>
            ))}
            <div className="flex gap-3 pt-2">
              <button onClick={closeModal} className="flex-1 btn-secondary">Cancel</button>
              <button onClick={handleSave} disabled={saving} className="flex-1 btn-primary flex items-center justify-center gap-2">
                {saving ? <Loader2 size={16} className="animate-spin" /> : <Save size={16} />}
                {editEntry ? 'Save Changes' : 'Add Entry'}
              </button>
            </div>
          </div>
        </Modal>
      )}

      {/* Delete confirm modal */}
      {deleteId && (
        <Modal title="Confirm Delete" onClose={() => setDeleteId(null)}>
          <p className="text-gray-600 mb-6">Are you sure you want to delete this fertilizer entry? This cannot be undone.</p>
          <div className="flex gap-3">
            <button onClick={() => setDeleteId(null)} className="flex-1 btn-secondary">Cancel</button>
            <button onClick={() => handleDelete(deleteId)} className="flex-1 btn-danger">Delete</button>
          </div>
        </Modal>
      )}
    </div>
  )
}
