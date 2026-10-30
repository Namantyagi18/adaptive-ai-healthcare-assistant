import React from 'react';

type BadgeVariant =
  | 'cyan'
  | 'emerald'
  | 'amber'
  | 'rose'
  | 'purple'
  | 'slate'
  | 'emergency'
  | 'urgent';

interface BadgeProps {
  children: React.ReactNode;
  variant?: BadgeVariant;
  className?: string;
  icon?: React.ReactNode;
  pulse?: boolean;
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = 'cyan',
  className = '',
  icon,
  pulse = false,
}) => {
  const variantStyles: Record<BadgeVariant, string> = {
    cyan: 'bg-cyan-950/60 text-cyan-400 border-cyan-500/30',
    emerald: 'bg-emerald-950/60 text-emerald-400 border-emerald-500/30',
    amber: 'bg-amber-950/60 text-amber-400 border-amber-500/30',
    rose: 'bg-rose-950/60 text-rose-400 border-rose-500/30',
    purple: 'bg-purple-950/60 text-purple-400 border-purple-500/30',
    slate: 'bg-slate-800/80 text-slate-300 border-slate-700',
    emergency: 'bg-red-950/80 text-red-300 border-red-500/60 font-semibold tracking-wide',
    urgent: 'bg-amber-950/80 text-amber-300 border-amber-500/60 font-semibold',
  };

  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border backdrop-blur-sm ${
        variantStyles[variant]
      } ${pulse ? 'animate-pulse' : ''} ${className}`}
    >
      {icon && <span className="shrink-0">{icon}</span>}
      <span>{children}</span>
    </span>
  );
};

