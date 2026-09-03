import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts'

export default function FertilizerChart({ data = [] }) {
  const chartData = data.map((d) => ({ name: d.fertilizer, Count: d.count }))

  return (
    <ResponsiveContainer width="100%" height={280}>
      <BarChart data={chartData} margin={{ top: 5, right: 20, left: 0, bottom: 40 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
        <XAxis
          dataKey="name"
          angle={-30}
          textAnchor="end"
          tick={{ fontSize: 11, fill: '#6b7280' }}
          interval={0}
        />
        <YAxis tick={{ fontSize: 11, fill: '#6b7280' }} />
        <Tooltip
          contentStyle={{ borderRadius: '8px', border: '1px solid #e5e7eb', fontSize: 12 }}
        />
        <Bar dataKey="Count" fill="#16a34a" radius={[6, 6, 0, 0]} maxBarSize={50} />
      </BarChart>
    </ResponsiveContainer>
  )
}
