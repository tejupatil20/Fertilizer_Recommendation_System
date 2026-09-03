import { Link, useNavigate } from 'react-router-dom'
import { Leaf, Zap, BarChart3, Shield, FileDown, ChevronRight, Sprout, FlaskConical } from 'lucide-react'

export default function Landing() {
  return (
    <div className="min-h-screen bg-white">
      {/* Top bar */}
      <nav className="bg-white border-b border-gray-100 px-6 py-4 flex justify-between items-center sticky top-0 z-50 shadow-sm">
        <div className="flex items-center gap-2">
          <div className="bg-primary-600 text-white p-2 rounded-lg">
            <Leaf size={20} />
          </div>
          <span className="text-xl font-bold text-primary-700">FertiSmart</span>
          <span className="text-xl font-bold text-gray-700"> AI</span>
        </div>
        <div className="flex items-center gap-3">
          <Link to="/login" className="text-sm font-medium text-gray-600 hover:text-primary-700 transition-colors">
            Login
          </Link>
          <Link to="/register" className="btn-primary text-sm py-2 px-4">
            Get Started
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-700 via-primary-600 to-secondary-600 text-white py-24 px-6">
        <div className="max-w-5xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-sm border border-white/20 rounded-full px-4 py-2 mb-8 text-sm font-medium">
            <Zap size={14} className="text-amber-300" />
            Powered by RandomForest ML + Google Gemini AI
          </div>
          <h1 className="text-5xl md:text-6xl font-extrabold leading-tight mb-6">
            AI-Powered Fertilizer
            <br />
            <span className="text-amber-300">Recommendations</span> for
            <br />
            Modern Farmers
          </h1>
          <p className="text-xl text-primary-100 max-w-3xl mx-auto mb-10 leading-relaxed">
            Enter your soil data and crop information to receive intelligent, growth-stage-aware
            fertilizer recommendations with precise dosage — backed by Machine Learning and Gemini AI.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/register" className="inline-flex items-center gap-2 bg-white text-primary-700 font-bold py-4 px-8 rounded-xl hover:bg-primary-50 transition-all shadow-lg hover:shadow-xl text-lg">
              Start Free Analysis
              <ChevronRight size={20} />
            </Link>
            <a href="#about" className="inline-flex items-center gap-2 border-2 border-white/40 text-white font-semibold py-4 px-8 rounded-xl hover:bg-white/10 transition-all text-lg">
              Learn More
            </a>
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="bg-primary-800 text-white py-10">
        <div className="max-w-5xl mx-auto px-6 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          {[
            { label: 'Major Crops Supported', value: '5+' },
            { label: 'Fertilizer Types', value: '7+' },
            { label: 'Growth Stages Tracked', value: '20+' },
            { label: 'AI-Powered', value: '100%' },
          ].map((stat) => (
            <div key={stat.label}>
              <div className="text-3xl font-extrabold text-amber-300">{stat.value}</div>
              <div className="text-sm text-primary-200 mt-1">{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* How it works */}
      <section id="about" className="py-20 px-6 bg-gray-50">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-14">
            <h2 className="text-3xl font-bold text-gray-900 mb-3">How It Works</h2>
            <p className="text-gray-500 text-lg">Three simple steps to smarter farming</p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                step: '01',
                title: 'Enter Soil Data',
                desc: 'Input your soil nitrogen, phosphorous, potassium levels, pH, temperature, humidity, rainfall, and days since planting.',
                icon: <FlaskConical size={28} className="text-primary-600" />,
              },
              {
                step: '02',
                title: 'AI Analysis',
                desc: 'Our RandomForest model analyzes your data against 5,000+ training samples. Gemini AI then enriches it with growth-stage reasoning.',
                icon: <Zap size={28} className="text-primary-600" />,
              },
              {
                step: '03',
                title: 'Get Recommendation',
                desc: 'Receive a precise fertilizer recommendation with dosage per acre, application method, timing advice, and a downloadable PDF report.',
                icon: <FileDown size={28} className="text-primary-600" />,
              },
            ].map((item) => (
              <div key={item.step} className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100 text-center hover:shadow-md transition-shadow">
                <div className="text-5xl font-black text-primary-100 mb-4">{item.step}</div>
                <div className="flex justify-center mb-4">
                  <div className="bg-primary-50 p-4 rounded-xl">{item.icon}</div>
                </div>
                <h3 className="text-lg font-bold text-gray-900 mb-2">{item.title}</h3>
                <p className="text-gray-500 text-sm leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20 px-6 bg-white">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-14">
            <h2 className="text-3xl font-bold text-gray-900 mb-3">Platform Features</h2>
            <p className="text-gray-500 text-lg">Everything you need for precision agriculture</p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              { icon: <BarChart3 size={24} />, title: 'RandomForest ML', desc: 'Trained on 5,000+ synthetic data points with 200 decision trees for accurate fertilizer prediction.' },
              { icon: <Zap size={24} />, title: 'Gemini AI Insights', desc: 'Natural language explanations from Google Gemini AI, tailored to crop growth stage and soil conditions.' },
              { icon: <Sprout size={24} />, title: 'Growth Stage Tracking', desc: 'Automatic detection of crop growth stage based on days since planting across 5 major crops.' },
              { icon: <FileDown size={24} />, title: 'PDF Reports', desc: 'Professional letterhead-quality PDF reports with application calendar, precautions, and farmer details.' },
              { icon: <BarChart3 size={24} />, title: 'Admin Analytics', desc: 'Rich dashboard with Recharts visualizations: fertilizer trends, crop queries, and prediction timelines.' },
              { icon: <Shield size={24} />, title: 'Secure JWT Auth', desc: 'Role-based access control with bcrypt password hashing and JWT tokens for farmers and admins.' },
            ].map((feature) => (
              <div key={feature.title} className="p-6 rounded-xl border border-gray-100 hover:border-primary-200 hover:shadow-sm transition-all group">
                <div className="text-primary-600 mb-3 group-hover:scale-110 transition-transform inline-block">{feature.icon}</div>
                <h3 className="font-bold text-gray-900 mb-2">{feature.title}</h3>
                <p className="text-gray-500 text-sm leading-relaxed">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Supported crops */}
      <section className="py-16 px-6 bg-primary-50">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-3">Crops Supported</h2>
          <p className="text-gray-500 mb-8">Complete growth stage data for major Indian crops</p>
          <div className="flex flex-wrap justify-center gap-3">
            {['🌾 Rice (Paddy)', '🌾 Wheat', '🌽 Maize', '🌿 Cotton', '🎋 Sugarcane', '🌱 Tobacco', '🌾 Barley', '🌿 Millets', '🫘 Pulses', '🌻 Oil Seeds', '🥜 Ground Nuts'].map((crop) => (
              <span key={crop} className="bg-white text-primary-700 font-medium px-5 py-2.5 rounded-full shadow-sm border border-primary-100 hover:border-primary-300 transition-colors text-sm">
                {crop}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-6 bg-gradient-to-r from-primary-700 to-secondary-600 text-white text-center">
        <div className="max-w-2xl mx-auto">
          <Leaf size={48} className="mx-auto mb-4 text-amber-300" />
          <h2 className="text-3xl font-bold mb-4">Ready to Optimize Your Farm?</h2>
          <p className="text-primary-100 mb-8 text-lg">Join farmers using AI to make smarter fertilizer decisions.</p>
          <Link to="/register" className="inline-flex items-center gap-2 bg-white text-primary-700 font-bold py-4 px-10 rounded-xl hover:bg-primary-50 transition-all shadow-lg text-lg">
            Create Free Account
            <ChevronRight size={20} />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-8 text-center text-sm">
        <p>© 2026 FertiSmart AI — Smart Fertilizer Recommendation System. Built with React, FastAPI, and ❤️</p>
      </footer>
    </div>
  )
}
