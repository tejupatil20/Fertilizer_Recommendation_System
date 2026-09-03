import { Leaf } from 'lucide-react'

export default function GrowthStageTimeline({ stages = [], currentDays = 0 }) {
  if (!stages || stages.length === 0) return null

  const currentStageIdx = stages.findIndex(
    (s) => s.min_days <= currentDays && s.max_days >= currentDays
  )

  return (
    <div className="overflow-x-auto py-2">
      <div className="flex items-start gap-0 min-w-max">
        {stages.map((stage, idx) => {
          const isActive = idx === currentStageIdx
          const isPast = idx < currentStageIdx

          return (
            <div key={stage.id || idx} className="flex items-start">
              {/* Stage node */}
              <div className="flex flex-col items-center w-28 text-center">
                <div
                  className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold border-2 transition-all ${
                    isActive
                      ? 'bg-primary-600 text-white border-primary-600 shadow-lg shadow-primary-200 scale-110'
                      : isPast
                      ? 'bg-primary-200 text-primary-700 border-primary-300'
                      : 'bg-white text-gray-400 border-gray-200'
                  }`}
                >
                  {isActive ? <Leaf size={16} /> : idx + 1}
                </div>
                <p className={`text-xs font-semibold mt-2 leading-tight ${isActive ? 'text-primary-700' : isPast ? 'text-gray-500' : 'text-gray-400'}`}>
                  {stage.stage_name}
                </p>
                <p className={`text-xs mt-0.5 ${isActive ? 'text-primary-500' : 'text-gray-400'}`}>
                  Day {stage.min_days}–{stage.max_days}
                </p>
                {isActive && (
                  <span className="mt-1 text-xs bg-primary-100 text-primary-700 px-2 py-0.5 rounded-full font-medium">
                    Current
                  </span>
                )}
              </div>

              {/* Connector line */}
              {idx < stages.length - 1 && (
                <div className={`h-0.5 w-8 mt-5 ${isPast || isActive ? 'bg-primary-300' : 'bg-gray-200'}`} />
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
