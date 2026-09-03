import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Leaf, Eye, EyeOff, Loader2, User, ShieldCheck } from 'lucide-react'
import toast from 'react-hot-toast'
import api from '../api/axios'

export default function Register() {
  const [form, setForm] = useState({ username: '', password: '', confirmPassword: '', role: 'farmer' })
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (form.username.length < 3) {
      toast.error('Username must be at least 3 characters')
      return
    }
    if (form.password.length < 6) {
      toast.error('Password must be at least 6 characters')
      return
    }
    if (form.password !== form.confirmPassword) {
      toast.error('Passwords do not match')
      return
    }
    setLoading(true)
    try {
      await api.post('/auth/register', {
        username: form.username,
        password: form.password,
        role: form.role,
      })
      toast.success('Account created successfully! Please log in.')
      navigate('/login')
    } catch (err) {
      const msg = err.response?.data?.detail || 'Registration failed. Please try again.'
      toast.error(msg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-emerald-50 flex items-center justify-center px-4 py-8">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-8 animate-slide-up">
          {/* Logo */}
          <div className="text-center mb-8">
            <Link to="/" className="inline-flex items-center gap-2 group">
              <div className="bg-primary-600 text-white p-3 rounded-xl group-hover:bg-primary-700 transition-colors">
                <Leaf size={24} />
              </div>
            </Link>
            <h1 className="text-2xl font-bold text-gray-900 mt-4">Create Account</h1>
            <p className="text-gray-500 mt-1 text-sm">Join FertiSmart AI today</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="label">Username</label>
              <input
                type="text"
                name="username"
                value={form.username}
                onChange={handleChange}
                placeholder="Choose a username (min 3 chars)"
                className="input-field"
                autoComplete="username"
                minLength={3}
                required
              />
            </div>

            <div>
              <label className="label">Password</label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="password"
                  value={form.password}
                  onChange={handleChange}
                  placeholder="Minimum 6 characters"
                  className="input-field pr-12"
                  autoComplete="new-password"
                  minLength={6}
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>

            <div>
              <label className="label">Confirm Password</label>
              <input
                type="password"
                name="confirmPassword"
                value={form.confirmPassword}
                onChange={handleChange}
                placeholder="Repeat your password"
                className="input-field"
                autoComplete="new-password"
                required
              />
            </div>

            {/* Role selection */}
            <div>
              <label className="label">Account Type</label>
              <div className="grid grid-cols-2 gap-3">
                {[
                  { value: 'farmer', label: 'Farmer', icon: <User size={18} />, desc: 'Get recommendations' },
                  { value: 'admin', label: 'Admin', icon: <ShieldCheck size={18} />, desc: 'Manage system' },
                ].map((option) => (
                  <button
                    key={option.value}
                    type="button"
                    onClick={() => setForm({ ...form, role: option.value })}
                    className={`flex flex-col items-center gap-1.5 p-4 rounded-xl border-2 transition-all ${
                      form.role === option.value
                        ? 'border-primary-600 bg-primary-50 text-primary-700'
                        : 'border-gray-200 text-gray-500 hover:border-gray-300'
                    }`}
                  >
                    {option.icon}
                    <span className="font-semibold text-sm">{option.label}</span>
                    <span className="text-xs opacity-70">{option.desc}</span>
                  </button>
                ))}
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full btn-primary flex items-center justify-center gap-2 py-3"
            >
              {loading ? (
                <>
                  <Loader2 size={18} className="animate-spin" />
                  Creating account...
                </>
              ) : (
                'Create Account'
              )}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-500">
              Already have an account?{' '}
              <Link to="/login" className="text-primary-600 font-semibold hover:text-primary-700">
                Sign in
              </Link>
            </p>
          </div>
        </div>

        <p className="text-center text-xs text-gray-400 mt-6">
          <Link to="/" className="hover:text-primary-600">← Back to Home</Link>
        </p>
      </div>
    </div>
  )
}
