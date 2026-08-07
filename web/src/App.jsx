import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { WeatherProvider } from './context/WeatherContext';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';
import { MobileBottomNav } from './components/MobileBottomNav';
import { FloatingChatButton } from './components/FloatingChatButton';
import { LocationPermissionModal } from './components/LocationPermissionModal';
import { ProtectedRoute } from './components/ProtectedRoute';
import { LandingPage } from './pages/LandingPage';
import { DashboardPage } from './pages/DashboardPage';
import { AiAssistantPage } from './pages/AiAssistantPage';
import { EmergencyPage } from './pages/EmergencyPage';
import { AlertHistoryPage } from './pages/AlertHistoryPage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { MapPage } from './pages/MapPage';
import { CommunityPage } from './pages/CommunityPage';
import { ComparisonPage } from './pages/ComparisonPage';
import { AlertsPage } from './pages/AlertsPage';
import { AdminPage } from './pages/AdminPage';
import { LoginPage } from './pages/LoginPage';
import { RegisterPage } from './pages/RegisterPage';

function AppLayout() {
  const { user } = useAuth();

  return (
    <div className="min-h-screen flex flex-col overflow-x-hidden max-w-full">
      <Navbar />
      <LocationPermissionModal />
      <div className="max-w-7xl mx-auto w-full px-3 sm:px-6 lg:px-8 flex-1 flex gap-6 pb-20 lg:pb-12">
        {user && <Sidebar />}
        <main className="flex-1 min-w-0 max-w-full overflow-x-hidden">
          <Routes>
            <Route path="/login" element={user ? <Navigate to="/dashboard" replace /> : <LoginPage />} />
            <Route path="/register" element={user ? <Navigate to="/dashboard" replace /> : <RegisterPage />} />
            
            {/* Protected Routes */}
            <Route path="/" element={<ProtectedRoute><LandingPage /></ProtectedRoute>} />
            <Route path="/dashboard" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
            <Route path="/ai-chat" element={<ProtectedRoute><AiAssistantPage /></ProtectedRoute>} />
            <Route path="/emergency" element={<ProtectedRoute><EmergencyPage /></ProtectedRoute>} />
            <Route path="/alert-history" element={<ProtectedRoute><AlertHistoryPage /></ProtectedRoute>} />
            <Route path="/analytics" element={<ProtectedRoute><AnalyticsPage /></ProtectedRoute>} />
            <Route path="/map" element={<ProtectedRoute><MapPage /></ProtectedRoute>} />
            <Route path="/community" element={<ProtectedRoute><CommunityPage /></ProtectedRoute>} />
            <Route path="/comparison" element={<ProtectedRoute><ComparisonPage /></ProtectedRoute>} />
            <Route path="/alerts" element={<ProtectedRoute><AlertsPage /></ProtectedRoute>} />
            <Route path="/admin" element={<ProtectedRoute><AdminPage /></ProtectedRoute>} />

            {/* Catch All Redirect */}
            <Route path="*" element={<Navigate to={user ? "/dashboard" : "/login"} replace />} />
          </Routes>
        </main>
      </div>
      {user && <MobileBottomNav />}
      {user && <FloatingChatButton />}
    </div>
  );
}

export function App() {
  return (
    <AuthProvider>
      <WeatherProvider>
        <Router>
          <AppLayout />
        </Router>
      </WeatherProvider>
    </AuthProvider>
  );
}

export default App;
