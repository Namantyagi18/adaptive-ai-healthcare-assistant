/**
 * ADAPT-AI Backend Health & Authentication State Context
 */

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { apiService, getDeveloperOverrideKey, setDeveloperOverrideKey } from '../services/api';
import { HealthStatus } from '../types';

interface AuthContextType {
  isBackendHealthy: boolean;
  healthData: HealthStatus | null;
  refreshHealth: () => Promise<void>;
  isLoadingHealth: boolean;
  developerKey: string | null;
  setDeveloperKey: (key: string | null) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [isBackendHealthy, setIsBackendHealthy] = useState<boolean>(false);
  const [healthData, setHealthData] = useState<HealthStatus | null>(null);
  const [isLoadingHealth, setIsLoadingHealth] = useState<boolean>(true);
  const [developerKey, setDevKeyState] = useState<string | null>(getDeveloperOverrideKey());

  const checkStatus = async () => {
    try {
      setIsLoadingHealth(true);
      const data = await apiService.getHealth();
      setHealthData(data);
      setIsBackendHealthy(data.status === 'healthy');
    } catch {
      setIsBackendHealthy(false);
      setHealthData(null);
    } finally {
      setIsLoadingHealth(false);
    }
  };

  useEffect(() => {
    checkStatus();
    const interval = setInterval(checkStatus, 30000); // 30s polling
    return () => clearInterval(interval);
  }, []);

  const updateDeveloperKey = (key: string | null) => {
    setDeveloperOverrideKey(key);
    setDevKeyState(key);
  };

  return (
    <AuthContext.Provider
      value={{
        isBackendHealthy,
        healthData,
        refreshHealth: checkStatus,
        isLoadingHealth,
        developerKey,
        setDeveloperKey: updateDeveloperKey,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return ctx;
};
