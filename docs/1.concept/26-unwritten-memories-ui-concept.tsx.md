```typescript
import React, { useState } from 'react';
import { BookOpen, Coffee, Dumbbell, Users, MapPin, Heart, Star, Zap, Clock, DollarSign, AlertCircle, Sparkles, Moon, Sun, Sunset, TrendingUp, Brain, Activity } from 'lucide-react';

const UnwrittenMemories = () => {
  const [selectedCard, setSelectedCard] = useState(null);
  const [plannedCards, setPlannedCards] = useState({
    morning: null,
    afternoon: null,
    evening: null
  });
  const [expandedCluster, setExpandedCluster] = useState(null);
  const [currentPhase, setCurrentPhase] = useState('morning');

  // Game State
  const gameState = {
    week: 1,
    day: 1,
    dayName: 'Monday',
    act: 1,
    
    emotionalState: {
      primary: 'MOTIVATED',
      intensity: 0.7,
      color: 'amber'
    },
    
    meters: {
      physical: 7,
      mental: 6,
      social: 8,
      emotional: 7
    },
    
    capacity: 7.2,
    activeStressors: 1,
    stressorDetails: ['Work deadline approaching'],
    burnout: 15,
    burnoutRecovery: 0.5,
    
    resources: {
      energy: 8,
      energyMax: 10,
      time: 3.0,
      money: 850,
      socialCapital: 12
    },
    
    aspiration: {
      name: "Launch Photography Business",
      progress: 15
    },
    
    activeHooks: 2,
    
    avatar: {
      mood: 'focused',
      outfit: 'casual'
    },
    
    currentScene: {
      location: "Your Apartment",
      time: "morning",
      lighting: "soft morning light through windows"
    }
  };

  const cards = [
    {
      id: 1,
      title: "Coffee Chat",
      type: "activity",
      illustration: Coffee,
      level: 2,
      desc: "The steam rises in lazy spirals. You could invite someone.",
      cost: { time: 0.5, energy: 1 },
      appeal: 1.8
    },
    {
      id: 2,
      title: "Gym Workout",
      type: "activity",
      illustration: Dumbbell,
      level: 1,
      desc: "Your reflection in the mirror waits for a decision.",
      cost: { time: 1, energy: 3 },
      appeal: 2.0
    },
    {
      id: 3,
      title: "Work on Portfolio",
      type: "aspiration",
      illustration: Sparkles,
      level: 3,
      desc: "Your aspiration calls. Progress awaits.",
      cost: { time: 2, energy: 2 },
      appeal: 2.5
    },
    {
      id: 4,
      title: "Sarah",
      type: "person",
      role: "Close Friend",
      illustration: Users,
      level: 3,
      trust: 4,
      desc: "She always knows when you need guidance.",
      cost: { time: 1, energy: 2 },
      appeal: 1.5
    },
    {
      id: 5,
      title: "Marcus",
      type: "person",
      role: "Best Friend",
      illustration: Users,
      level: 2,
      trust: 3,
      desc: "Easy laughter and old memories.",
      cost: { time: 1, energy: 1 },
      appeal: 1.3
    },
    {
      id: 6,
      title: "Local Park",
      type: "location",
      illustration: MapPin,
      level: 1,
      desc: "Morning light filters through the leaves.",
      cost: { time: 0.5, energy: 1 },
      appeal: 1.0
    },
    {
      id: 7,
      title: "Research Equipment",
      type: "aspiration",
      illustration: TrendingUp,
      level: 2,
      desc: "Better gear means better shots. Investment time.",
      cost: { time: 1.5, energy: 1 },
      appeal: 2.2
    },
    {
      id: 8,
      title: "Rest & Recharge",
      type: "recovery",
      illustration: Moon,
      level: 1,
      desc: "Sometimes doing nothing is doing something.",
      cost: { time: 2, energy: -3 },
      appeal: 0.7
    }
  ];

  const MeterDisplay = ({ label, value, max = 10, color, icon: Icon }) => (
    <div className="flex items-center gap-2 mb-2">
      <div className="w-6 h-6 rounded-full bg-stone-800/40 flex items-center justify-center">
        <Icon className="w-3 h-3 text-stone-400" />
      </div>
      <div className="flex-1">
        <div className="text-[9px] uppercase tracking-wider text-stone-400 mb-0.5" style={{ fontVariant: 'small-caps' }}>
          {label}
        </div>
        <div className="flex gap-0.5">
          {[...Array(max)].map((_, i) => (
            <div
              key={i}
              className={`w-1.5 h-1.5 rounded-full ${
                i < value ? color : 'bg-stone-700/30'
              }`}
            />
          ))}
        </div>
      </div>
      <div className="text-xs text-stone-300 font-light w-8 text-right">{value}/{max}</div>
    </div>
  );

  const Cluster = ({ id, title, collapsedContent, expandedContent, className = "" }) => {
    const isExpanded = expandedCluster === id;
    
    return (
      <div 
        className={`bg-stone-800/60 backdrop-blur-md rounded-lg border border-stone-700/50 transition-all duration-300 cursor-pointer ${className} ${
          isExpanded ? 'shadow-xl' : 'shadow-md'
        }`}
        onClick={(e) => {
          e.stopPropagation();
          setExpandedCluster(isExpanded ? null : id);
        }}
      >
        {isExpanded ? (
          <div className="p-4" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-3">
              <div className="text-xs uppercase tracking-wider text-stone-400 font-medium">
                {title}
              </div>
              <button 
                className="text-[10px] text-stone-500 hover:text-stone-300"
                onClick={(e) => {
                  e.stopPropagation();
                  setExpandedCluster(null);
                }}
              >
                tap to collapse
              </button>
            </div>
            {expandedContent}
          </div>
        ) : (
          <div className="p-3 hover:bg-stone-700/20 transition-colors group">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                {collapsedContent}
              </div>
              <div className="text-stone-600 group-hover:text-stone-400 transition-colors">
                <BookOpen className="w-3 h-3" />
              </div>
            </div>
          </div>
        )}
      </div>
    );
  };

  const Card = ({ card, index, isInHand = true }) => {
    const Icon = card.illustration;
    const isSelected = selectedCard?.id === card.id;
    
    const totalCards = cards.length;
    const middleIndex = totalCards / 2;
    const distanceFromMiddle = index - middleIndex;
    const rotation = isInHand ? distanceFromMiddle * 3 : 0;
    const yOffset = isInHand ? Math.abs(distanceFromMiddle) * 4 : 0;
    const zIndex = isInHand ? (isSelected ? 100 : 50 - Math.abs(distanceFromMiddle)) : 'auto';

    const levelColors = [
      'from-stone-200 to-stone-100',
      'from-amber-100 to-stone-100',
      'from-amber-200 to-amber-100',
      'from-yellow-300 to-amber-200',
      'from-yellow-400 to-yellow-300'
    ];

    const stateGlow = card.appeal > 2.0 ? 'shadow-amber-500/20' : '';

    return (
      <div
        onClick={(e) => {
          e.stopPropagation();
          setSelectedCard(card);
        }}
        style={{
          transform: isInHand 
            ? `rotate(${rotation}deg) translateY(${isSelected ? -40 : yOffset}px)`
            : 'none',
          zIndex: zIndex,
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
        }}
        className={`w-32 h-44 relative cursor-pointer group ${isInHand ? 'absolute' : ''}`}
      >
        <div className="absolute inset-0 bg-stone-900 opacity-30 blur-md translate-y-2 rounded-sm"></div>
        
        <div className={`relative h-full bg-gradient-to-b ${levelColors[card.level] || levelColors[0]} 
          rounded-sm overflow-hidden border border-stone-300/50
          shadow-lg ${stateGlow} ${isSelected ? 'ring-2 ring-amber-500' : ''}`}
          style={{
            boxShadow: isSelected 
              ? '0 0 20px rgba(251, 191, 36, 0.4), 0 4px 12px rgba(0,0,0,0.3)' 
              : '0 2px 8px rgba(0,0,0,0.15)',
            backgroundImage: 'url("data:image/svg+xml,%3Csvg width="100" height="100" xmlns="http://www.w3.org/2000/svg"%3E%3Cfilter id="noise"%3E%3CfeTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4" /%3E%3CfeColorMatrix type="saturate" values="0"/%3E%3C/filter%3E%3Crect width="100" height="100" filter="url(%23noise)" opacity="0.03"/%3E%3C/svg%3E")',
          }}
        >
          <div className="absolute top-0 right-0 w-6 h-6 overflow-hidden">
            <div className="absolute top-0 right-0 w-8 h-8 bg-stone-400/30 transform rotate-45 translate-x-3 -translate-y-3"></div>
          </div>

          {card.appeal > 1.8 && (
            <div className="absolute top-1 left-1 w-4 h-4 rounded-full bg-amber-500/80 flex items-center justify-center">
              <Sparkles className="w-2 h-2 text-white" />
            </div>
          )}

          {card.type === 'person' && card.trust && (
            <div className="absolute top-2 right-2 flex gap-0.5">
              {[...Array(5)].map((_, i) => (
                <div
                  key={i}
                  className={`w-1 h-1 rounded-full ${
                    i < card.trust ? 'bg-amber-600' : 'bg-stone-300/40'
                  }`}
                />
              ))}
            </div>
          )}

          <div className="h-3/5 flex items-center justify-center relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-stone-900/5"></div>
            
            <Icon 
              className="w-12 h-12 text-stone-600/40 stroke-[0.5px]"
              style={{ filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.1))' }}
            />
            
            <div className="absolute bottom-1 right-1 flex gap-0.5">
              {[...Array(card.level)].map((_, i) => (
                <Star key={i} className="w-1.5 h-1.5 fill-amber-600 text-amber-600" />
              ))}
            </div>
          </div>

          <div className="h-2/5 px-2 py-1.5 bg-gradient-to-b from-stone-50/90 to-stone-100/90 backdrop-blur-sm border-t border-stone-300/30">
            <h3 className="text-xs font-medium text-stone-800 mb-0.5 leading-tight">
              {card.title}
              {card.role && <span className="text-[10px] text-stone-500 ml-1">({card.role})</span>}
            </h3>
            <p className="text-[9px] text-stone-600 leading-snug italic opacity-80 line-clamp-2">
              {card.desc}
            </p>
            
            <div className="flex gap-1.5 mt-1 text-[9px] text-stone-500">
              <span>⏱ {card.cost.time}h</span>
              <span>⚡ {card.cost.energy}</span>
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="w-full h-screen overflow-hidden relative bg-stone-900"
      style={{
        backgroundImage: `
          linear-gradient(to bottom, rgba(28, 25, 23, 0.95), rgba(28, 25, 23, 0.85)),
          url("data:image/svg+xml,%3Csvg width='100' height='100' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100' height='100' filter='url(%23noise)' opacity='0.4'/%3E%3C/svg%3E")
        `,
        backgroundSize: 'cover',
        backgroundPosition: 'center'
      }}
    >
      <div className="absolute inset-0 flex items-center justify-center opacity-10 pointer-events-none">
        <div className="text-9xl font-light text-stone-400">
          {gameState.currentScene.location}
        </div>
      </div>

      <div className="absolute top-3 left-1/2 -translate-x-1/2 z-5">
        <div className="text-[10px] text-stone-600 italic flex items-center gap-1">
          <BookOpen className="w-3 h-3" />
          <span>Tap clusters to reveal details</span>
        </div>
      </div>

      <div className="absolute left-0 top-1/3 -translate-y-1/2 flex flex-col gap-2 z-20">
        {['morning', 'afternoon', 'evening'].map((phase) => {
          const PhaseIcon = phase === 'morning' ? Sun : phase === 'afternoon' ? Sunset : Moon;
          const isActive = currentPhase === phase;
          
          return (
            <button
              key={phase}
              onClick={(e) => {
                e.stopPropagation();
                setCurrentPhase(phase);
              }}
              className={`w-10 h-16 rounded-r-lg border-r border-t border-b transition-all ${
                isActive 
                  ? 'bg-amber-700/90 border-amber-600 translate-x-0' 
                  : 'bg-stone-800/60 border-stone-700/50 -translate-x-8 hover:translate-x-0'
              }`}
            >
              <PhaseIcon className={`w-5 h-5 mx-auto ${isActive ? 'text-stone-100' : 'text-stone-400'}`} />
            </button>
          );
        })}
      </div>

      <div className="relative z-10 h-14 px-6 pt-3 flex items-start justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-amber-500 to-amber-700 flex items-center justify-center text-xl border-2 border-amber-600/50">
            👤
          </div>
          
          <div>
            <div className="flex items-center gap-2">
              <span className="text-sm font-medium text-stone-200">
                Week {gameState.week}, Day {gameState.day}
              </span>
              <span className="text-xs text-stone-400">•</span>
              <span className="text-xs text-stone-400">{gameState.dayName}</span>
            </div>
            <div className="flex items-center gap-2 mt-0.5">
              <span className="text-xs font-medium text-amber-400">{gameState.emotionalState.primary}</span>
              <div className="flex gap-0.5">
                {[...Array(5)].map((_, i) => (
                  <div
                    key={i}
                    className={`w-1 h-2 rounded-full ${
                      i < gameState.emotionalState.intensity * 5 ? 'bg-amber-500' : 'bg-stone-700/30'
                    }`}
                  />
                ))}
              </div>
            </div>
          </div>

          <div className="ml-4 flex items-center gap-2">
            <span className="text-[10px] text-stone-500 uppercase tracking-wide">Act {gameState.act}</span>
            <div className="flex gap-1">
              {[...Array(3)].map((_, i) => (
                <div
                  key={i}
                  className={`w-8 h-1 rounded-full ${
                    i === 0 ? 'bg-amber-600' : 'bg-stone-700/30'
                  }`}
                />
              ))}
            </div>
          </div>
        </div>

        <div className="bg-stone-800/40 backdrop-blur-sm px-4 py-2 rounded-md border border-stone-700/50">
          <div className="text-[10px] text-stone-500 uppercase tracking-wide mb-1" style={{ fontVariant: 'small-caps' }}>
            {gameState.aspiration.name}
          </div>
          <div className="flex items-center gap-2">
            <div className="w-32 h-1.5 bg-stone-700/30 rounded-full overflow-hidden">
              <div 
                className="h-full bg-gradient-to-r from-amber-600 to-amber-500 rounded-full transition-all"
                style={{ width: `${gameState.aspiration.progress}%` }}
              />
            </div>
            <span className="text-xs text-stone-300">{gameState.aspiration.progress}%</span>
          </div>
        </div>
      </div>

      <div className="absolute left-6 top-20 w-64 space-y-2 max-h-[calc(100vh-20rem)] overflow-y-auto">
        <Cluster
          id="character"
          title="CHARACTER STATE"
          collapsedContent={
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Heart className="w-4 h-4 text-amber-500" />
                <div>
                  <div className="text-xs font-medium text-amber-400">{gameState.emotionalState.primary}</div>
                  <div className="text-[10px] text-stone-400">Capacity: {gameState.capacity}/10</div>
                </div>
              </div>
            </div>
          }
          expandedContent={
            <div className="space-y-3">
              <div>
                <div className="text-sm font-medium text-amber-400 mb-1">
                  {gameState.emotionalState.primary}
                </div>
                <div className="text-xs text-stone-400">Intensity: {(gameState.emotionalState.intensity * 100).toFixed(0)}%</div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs text-stone-400">Emotional Capacity</span>
                  <span className="text-sm font-medium text-stone-200">{gameState.capacity}/10</span>
                </div>
                <div className="w-full h-2 bg-stone-700/30 rounded-full overflow-hidden">
                  <div 
                    className={`h-full rounded-full transition-all ${
                      gameState.capacity >= 6 ? 'bg-green-500' :
                      gameState.capacity >= 4 ? 'bg-yellow-500' :
                      gameState.capacity >= 2 ? 'bg-orange-500' : 'bg-red-500'
                    }`}
                    style={{ width: `${(gameState.capacity / 10) * 100}%` }}
                  />
                </div>
                <div className="text-[10px] text-stone-500 mt-1">
                  {gameState.capacity >= 6 ? 'HIGH - Can handle emotional demands' :
                   gameState.capacity >= 4 ? 'MODERATE - Manageable stress levels' :
                   gameState.capacity >= 2 ? 'LOW - Limited bandwidth' : 'DEPLETED - Critical'}
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs text-stone-400">Active Stressors</span>
                  <span className={`text-xs font-medium px-2 py-0.5 rounded ${
                    gameState.activeStressors >= 4 ? 'bg-red-500/20 text-red-400' :
                    gameState.activeStressors >= 3 ? 'bg-orange-500/20 text-orange-400' :
                    'bg-green-500/20 text-green-400'
                  }`}>
                    {gameState.activeStressors}/5
                  </span>
                </div>
                {gameState.stressorDetails.map((stressor, i) => (
                  <div key={i} className="text-[10px] text-stone-500 ml-2">• {stressor}</div>
                ))}
              </div>

              <div>
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs text-stone-400">Burnout Level</span>
                  <span className="text-xs font-medium text-stone-200">{gameState.burnout}/100</span>
                </div>
                <div className="w-full h-1.5 bg-stone-700/30 rounded-full overflow-hidden">
                  <div 
                    className={`h-full rounded-full transition-all ${
                      gameState.burnout < 25 ? 'bg-green-500' :
                      gameState.burnout < 50 ? 'bg-yellow-500' :
                      gameState.burnout < 75 ? 'bg-orange-500' : 'bg-red-500'
                    }`}
                    style={{ width: `${gameState.burnout}%` }}
                  />
                </div>
                <div className="text-[10px] text-stone-500 mt-1">
                  Recovery: +{gameState.burnoutRecovery}/week
                </div>
              </div>

              <div className="pt-2 border-t border-stone-700/50">
                <div className="text-[10px] text-amber-500 flex items-start gap-1">
                  <Sparkles className="w-3 h-3 mt-0.5 flex-shrink-0" />
                  <span>Balance work and rest to maintain capacity</span>
                </div>
              </div>
            </div>
          }
        />

        <Cluster
          id="meters"
          title="LIFE METERS"
          collapsedContent={
            <div className="grid grid-cols-2 gap-x-3 gap-y-1">
              <div className="flex items-center gap-1.5">
                <Activity className="w-3 h-3 text-green-500" />
                <span className="text-xs text-stone-300">Physical: {gameState.meters.physical}</span>
              </div>
              <div className="flex items-center gap-1.5">
                <Brain className="w-3 h-3 text-blue-500" />
                <span className="text-xs text-stone-300">Mental: {gameState.meters.mental}</span>
              </div>
              <div className="flex items-center gap-1.5">
                <Users className="w-3 h-3 text-purple-500" />
                <span className="text-xs text-stone-300">Social: {gameState.meters.social}</span>
              </div>
              <div className="flex items-center gap-1.5">
                <Heart className="w-3 h-3 text-amber-500" />
                <span className="text-xs text-stone-300">Emotional: {gameState.meters.emotional}</span>
              </div>
            </div>
          }
          expandedContent={
            <div className="space-y-2">
              <MeterDisplay label="Physical" value={gameState.meters.physical} color="bg-green-500" icon={Activity} />
              <div className="text-[10px] text-stone-500 ml-8 -mt-1 mb-2">
                Energized • Safe for 8+ turns
              </div>
              
              <MeterDisplay label="Mental" value={gameState.meters.mental} color="bg-blue-500" icon={Brain} />
              <div className="text-[10px] text-stone-500 ml-8 -mt-1 mb-2">
                Stable • Consider rest if working hard
              </div>
              
              <MeterDisplay label="Social" value={gameState.meters.social} color="bg-purple-500" icon={Users} />
              <div className="text-[10px] text-stone-500 ml-8 -mt-1 mb-2">
                Thriving • Can skip social for 2-3 weeks
              </div>
              
              <MeterDisplay label="Emotional" value={gameState.meters.emotional} color="bg-amber-500" icon={Heart} />
              <div className="text-[10px] text-stone-500 ml-8 -mt-1 mb-2">
                Fulfilled • Resilient to setbacks
              </div>

              <div className="pt-2 border-t border-stone-700/50">
                <div className="text-[10px] text-amber-500 flex items-start gap-1">
                  <Sparkles className="w-3 h-3 mt-0.5 flex-shrink-0" />
                  <span>Keep Mental above 5 this week</span>
                </div>
              </div>
            </div>
          }
        />

        <Cluster
          id="progress"
          title="PROGRESS & STORY"
          collapsedContent={
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-amber-500" />
                <div>
                  <div className="text-xs font-medium text-stone-300">Photography: {gameState.aspiration.progress}%</div>
                  <div className="text-[10px] text-stone-400">{gameState.activeHooks} Active Hooks</div>
                </div>
              </div>
            </div>
          }
          expandedContent={
            <div className="space-y-3">
              <div>
                <div className="text-xs font-medium text-stone-300 mb-2">
                  📸 {gameState.aspiration.name}
                </div>
                <div className="w-full h-2 bg-stone-700/30 rounded-full overflow-hidden mb-1">
                  <div 
                    className="h-full bg-gradient-to-r from-amber-600 to-amber-500 rounded-full transition-all"
                    style={{ width: `${gameState.aspiration.progress}%` }}
                  />
                </div>
                <div className="text-[10px] text-stone-500">
                  Next Milestone: 25% - First paid gig completed
                </div>
              </div>

              <div>
                <div className="text-xs text-stone-400 mb-1">Active Hooks ({gameState.activeHooks})</div>
                <div className="space-y-1.5">
                  <div className="text-[10px] text-stone-500 ml-2">
                    • ❓ Why has Sarah been distant? (5 weeks)
                  </div>
                  <div className="text-[10px] text-stone-500 ml-2">
                    • 🎯 Gallery contact intro promised (2 weeks)
                  </div>
                </div>
              </div>

              <div className="pt-2 border-t border-stone-700/50">
                <div className="text-[10px] text-amber-500 flex items-start gap-1">
                  <Sparkles className="w-3 h-3 mt-0.5 flex-shrink-0" />
                  <span>Focus on building portfolio quality this week</span>
                </div>
              </div>
            </div>
          }
        />
      </div>

      <div className="absolute right-6 top-20 w-56 space-y-2">
        <Cluster
          id="resources"
          title="RESOURCES"
          collapsedContent={
            <div className="grid grid-cols-2 gap-2">
              <div className="flex items-center gap-1.5">
                <Zap className="w-3 h-3 text-amber-500" />
                <span className="text-xs text-stone-300">{gameState.resources.energy}/{gameState.resources.energyMax}</span>
              </div>
              <div className="flex items-center gap-1.5">
                <Clock className="w-3 h-3 text-blue-500" />
                <span className="text-xs text-stone-300">{gameState.resources.time}h</span>
              </div>
              <div className="flex items-center gap-1.5">
                <DollarSign className="w-3 h-3 text-green-500" />
                <span className="text-xs text-stone-300">${gameState.resources.money}</span>
              </div>
              <div className="flex items-center gap-1.5">
                <Users className="w-3 h-3 text-purple-500" />
                <span className="text-xs text-stone-300">{gameState.resources.socialCapital}</span>
              </div>
            </div>
          }
          expandedContent={
            <div className="space-y-3">
              <div>
                <div className="flex items-center justify-between mb-1">
                  <div className="flex items-center gap-2">
                    <Zap className="w-4 h-4 text-amber-500" />
                    <span className="text-xs text-stone-400">Energy</span>
                  </div>
                  <span className="text-sm font-medium text-stone-200">
                    {gameState.resources.energy}/{gameState.resources.energyMax}
                  </span>
                </div>
                <div className="w-full h-1.5 bg-stone-700/30 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-amber-500 rounded-full"
                    style={{ width: `${(gameState.resources.energy / gameState.resources.energyMax) * 100}%` }}
                  />
                </div>
                <div className="text-[10px] text-stone-500 mt-1">
                  Regenerates +8 per night
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Clock className="w-4 h-4 text-blue-500" />
                    <span className="text-xs text-stone-400">Time Left</span>
                  </div>
                  <span className="text-sm font-medium text-stone-200">{gameState.resources.time}h</span>
                </div>
                <div className="text-[10px] text-stone-500 mt-1">
                  {currentPhase === 'morning' ? 'Morning phase (4h total)' :
                   currentPhase === 'afternoon' ? 'Afternoon phase (4h total)' :
                   'Evening phase (4h total)'}
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-1">
                  <div className="flex items-center gap-2">
                    <DollarSign className="w-4 h-4 text-green-500" />
                    <span className="text-xs text-stone-400">Money</span>
                  </div>
                  <span className="text-sm font-medium text-stone-200">${gameState.resources.money}</span>
                </div>
                <div className="text-[10px] text-stone-500">
                  Rent due Week 3: $1,200
                </div>
                <div className="text-[10px] text-amber-400 mt-1">
                  ⚠️ Need $350 more
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Users className="w-4 h-4 text-purple-500" />
                    <span className="text-xs text-stone-400">Social Capital</span>
                  </div>
                  <span className="text-sm font-medium text-stone-200">{gameState.resources.socialCapital}</span>
                </div>
                <div className="text-[10px] text-stone-500 mt-1">
                  Can ask favors from close friends
                </div>
              </div>
            </div>
          }
        />

        <Cluster
          id="timeline"
          title="TIMELINE"
          collapsedContent={
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <BookOpen className="w-4 h-4 text-amber-500" />
                <div>
                  <div className="text-xs font-medium text-stone-300">Week {gameState.week}, Day {gameState.day}</div>
                  <div className="text-[10px] text-stone-400">Act I - Setup</div>
                </div>
              </div>
            </div>
          }
          expandedContent={
            <div className="space-y-3">
              <div>
                <div className="text-xs text-stone-400 mb-1">Current Position</div>
                <div className="text-sm font-medium text-stone-300">
                  Week {gameState.week}, Day {gameState.day} - {gameState.dayName}
                </div>
                <div className="text-[10px] text-stone-500">Season Length: 24 weeks</div>
              </div>

              <div>
                <div className="text-xs text-stone-400 mb-2">Act Structure</div>
                <div className="space-y-1.5">
                  <div>
                    <div className="flex items-center justify-between text-[10px] mb-0.5">
                      <span className="text-stone-400">Act I: Setup</span>
                      <span className="text-stone-500">Weeks 1-6</span>
                    </div>
                    <div className="w-full h-1 bg-stone-700/30 rounded-full overflow-hidden">
                      <div className="w-1/6 h-full bg-amber-500 rounded-full" />
                    </div>
                  </div>
                  <div className="text-[10px] text-stone-500">
                    Act II: Complications (Weeks 7-18)
                  </div>
                  <div className="text-[10px] text-stone-500">
                    Act III: Resolution (Weeks 19-24)
                  </div>
                </div>
              </div>

              <div>
                <div className="text-xs text-stone-400 mb-1">This Week</div>
                <div className="space-y-0.5 text-[10px] text-stone-500">
                  <div>• Day 1: ← You are here</div>
                  <div>• Day 3: Client meeting</div>
                  <div>• Day 5: Sarah coffee date</div>
                </div>
              </div>

              <div className="pt-2 border-t border-stone-700/50">
                <div className="text-[10px] text-amber-500 flex items-start gap-1">
                  <Sparkles className="w-3 h-3 mt-0.5 flex-shrink-0" />
                  <span>Focus on building momentum</span>
                </div>
              </div>
            </div>
          }
        />
      </div>

      {(gameState.capacity < 3.0 || gameState.activeStressors >= 4 || gameState.burnout > 75 || 
        Object.values(gameState.meters).some(v => v <= 2)) && (
        <div className="absolute top-20 left-1/2 -translate-x-1/2 z-30">
          <div className="bg-red-900/90 backdrop-blur-sm border border-red-700 rounded-lg px-4 py-2 shadow-xl">
            <div className="flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-red-300" />
              <div className="text-sm text-red-100">
                {gameState.capacity < 3.0 && <div>⚠️ Emotional capacity critically low</div>}
                {gameState.activeStressors >= 4 && <div>🚨 Too many stressors active</div>}
                {gameState.burnout > 75 && <div>🔥 Severe burnout warning</div>}
                {Object.values(gameState.meters).some(v => v <= 2) && <div>💔 Critical meter alert</div>}
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="absolute left-1/2 top-36 -translate-x-1/2 w-[500px]">
        <div className="bg-stone-800/30 backdrop-blur-sm rounded-lg p-4 border border-stone-700/30">
          <div className="text-center mb-3">
            <div className="text-xs text-stone-400">Current Phase: {currentPhase.charAt(0).toUpperCase() + currentPhase.slice(1)}</div>
          </div>
          
          <div className="flex gap-3 justify-center">
            {['morning', 'afternoon', 'evening'].map((phase) => {
              const PhaseIcon = phase === 'morning' ? Sun : phase === 'afternoon' ? Sunset : Moon;
              const isActive = currentPhase === phase;
              
              return (
                <div 
                  key={phase} 
                  className={`w-32 bg-stone-900/50 rounded-lg p-2 border-2 ${
                    isActive ? 'border-amber-600' : 'border-dashed border-stone-700/50'
                  } min-h-[120px] flex flex-col items-center justify-center`}
                >
                  <PhaseIcon className={`w-5 h-5 mb-1 ${isActive ? 'text-amber-500' : 'text-stone-500'}`} />
                  <div className={`text-[10px] capitalize mb-2 ${isActive ? 'text-amber-400' : 'text-stone-500'}`}>
                    {phase}
                  </div>
                  {plannedCards[phase] && (
                    <div className="text-[9px] text-stone-400 text-center">
                      {plannedCards[phase].title}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </div>

      <div className="absolute bottom-20 left-0 right-0 h-64 flex items-end justify-center">
        <div className="relative w-[800px] h-48">
          {cards.map((card, index) => (
            <div
              key={card.id}
              style={{
                left: `${(index / (cards.length - 1)) * 100}%`,
                transform: 'translateX(-50%)'
              }}
              className="absolute bottom-0"
            >
              <Card card={card} index={index} />
            </div>
          ))}
        </div>
      </div>

      <div className="absolute bottom-0 left-0 right-0 h-20 px-6 flex items-center justify-between bg-gradient-to-t from-stone-900 via-stone-900/95 to-transparent">
        <div className="flex gap-3">
          <button className="flex items-center gap-2 px-4 py-2 bg-stone-800/80 hover:bg-stone-700 text-stone-200 rounded-md transition-colors border border-stone-700/50 text-sm">
            <BookOpen className="w-4 h-4" />
            <span>Draw (10)</span>
          </button>
          
          {selectedCard && (
            <button 
              onClick={(e) => {
                e.stopPropagation();
                setPlannedCards({...plannedCards, [currentPhase]: selectedCard});
                setSelectedCard(null);
              }}
              className="px-4 py-2 bg-amber-700 hover:bg-amber-600 text-stone-100 rounded-md transition-colors text-sm font-medium"
            >
              Commit to {currentPhase.charAt(0).toUpperCase() + currentPhase.slice(1)}
            </button>
          )}
        </div>

        <div className="text-sm text-stone-400 italic">
          {selectedCard 
            ? `"${selectedCard.title}" - ${selectedCard.cost.time}h, ${selectedCard.cost.energy} energy` 
            : 'Select a card to plan your turn'}
        </div>

        <div>
          <button className="px-6 py-2 bg-green-800 hover:bg-green-700 text-stone-100 rounded-md transition-colors text-sm font-medium border border-green-700">
            End Turn →
          </button>
        </div>
      </div>

      <div className="absolute inset-0 pointer-events-none"
        style={{
          background: 'radial-gradient(circle at center, transparent 40%, rgba(0, 0, 0, 0.5) 100%)'
        }}
      />
    </div>
  );
};

export default UnwrittenMemories;
```