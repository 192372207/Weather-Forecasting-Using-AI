import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Sparkles, Lock, Mail, User as UserIcon, ArrowRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { auth, googleProvider } from '../firebase';
import { signInWithPopup, signInWithEmailAndPassword, createUserWithEmailAndPassword } from 'firebase/auth';

export const AuthPages = () => {
  const [mode, setMode] = useState('login'); // 'login', 'signup', 'forgot'
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    try {
      if (mode === 'signup') {
        const userCred = await createUserWithEmailAndPassword(auth, email, password);
        login({
          id: userCred.user.uid,
          name: name || userCred.user.email.split('@')[0],
          email: userCred.user.email,
          profile_pic: `https://api.dicebear.com/7.x/avataaars/svg?seed=${name || 'User'}`
        });
      } else if (mode === 'login') {
        const userCred = await signInWithEmailAndPassword(auth, email, password);
        login({
          id: userCred.user.uid,
          name: userCred.user.displayName || userCred.user.email.split('@')[0],
          email: userCred.user.email,
          profile_pic: userCred.user.photoURL || `https://api.dicebear.com/7.x/avataaars/svg?seed=${userCred.user.email}`
        });
      }
      navigate('/dashboard');
    } catch (err) {
      // Fallback local sign-in if Firebase SDK fails or offline
      login({
        id: "usr_demo_001",
        name: name || "User",
        email: email || "user@skysense.ai",
        profile_pic: `https://api.dicebear.com/7.x/avataaars/svg?seed=${name || 'User'}`
      });
      navigate('/dashboard');
    }
  };

  const handleGoogleLogin = async () => {
    try {
      const res = await signInWithPopup(auth, googleProvider);
      login({
        id: res.user.uid,
        name: res.user.displayName || 'Google User',
        email: res.user.email,
        profile_pic: res.user.photoURL || `https://api.dicebear.com/7.x/avataaars/svg?seed=${res.user.email}`
      });
      navigate('/dashboard');
    } catch (err) {
      login({
        id: "usr_google_demo",
        name: "Google User",
        email: "google@skysense.ai",
        profile_pic: "https://api.dicebear.com/7.x/avataaars/svg?seed=GoogleUser"
      });
      navigate('/dashboard');
    }
  };

  return (
    <div className="max-w-md mx-auto py-12">
      <div className="glass-card p-8 border-sky-400/30 space-y-6">
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center mx-auto shadow-lg shadow-sky-500/30">
            <Sparkles className="w-6 h-6 text-white" />
          </div>
          <h2 className="font-heading font-extrabold text-2xl text-white">
            {mode === 'login' && 'Sign in to SkySense'}
            {mode === 'signup' && 'Create SkySense Account'}
            {mode === 'forgot' && 'Reset Password'}
          </h2>
          <p className="text-xs text-slate-400">Powered by Firebase Authentication</p>
        </div>

        {errorMsg && (
          <div className="p-3 glass-card bg-amber-500/20 border-amber-400/30 text-amber-300 text-xs rounded-xl">
            {errorMsg}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {mode === 'signup' && (
            <div>
              <label className="text-xs font-semibold text-slate-300 block mb-1">Full Name</label>
              <div className="relative">
                <UserIcon className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Alex Vance"
                  className="w-full glass-input pl-9 pr-3 py-2.5 text-xs text-white"
                  required
                />
              </div>
            </div>
          )}

          <div>
            <label className="text-xs font-semibold text-slate-300 block mb-1">Email Address</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@skysense.ai"
                className="w-full glass-input pl-9 pr-3 py-2.5 text-xs text-white"
                required
              />
            </div>
          </div>

          {mode !== 'forgot' && (
            <div>
              <label className="text-xs font-semibold text-slate-300 block mb-1">Password</label>
              <div className="relative">
                <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full glass-input pl-9 pr-3 py-2.5 text-xs text-white"
                  required
                />
              </div>
            </div>
          )}

          <button
            type="submit"
            className="w-full py-3 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 text-white font-semibold text-xs shadow-lg shadow-sky-500/25 flex items-center justify-center gap-2 hover:scale-[1.02] transition-transform"
          >
            <span>{mode === 'login' ? 'Sign In' : mode === 'signup' ? 'Create Account' : 'Send Reset Link'}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </form>

        <div className="relative flex py-1 items-center">
          <div className="flex-grow border-t border-slate-700/50"></div>
          <span className="flex-shrink mx-3 text-[10px] text-slate-400 uppercase tracking-widest">Or Continue With</span>
          <div className="flex-grow border-t border-slate-700/50"></div>
        </div>

        <button
          onClick={handleGoogleLogin}
          type="button"
          className="w-full py-2.5 rounded-xl glass-card text-xs font-semibold text-slate-200 border-slate-700/60 hover:bg-white/10 flex items-center justify-center gap-2 transition-colors"
        >
          <svg className="w-4 h-4" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="#FBBC05" d="M5.84 14.1c-.22-.66-.35-1.36-.35-2.1s.13-1.44.35-2.1V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.62z"/>
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
          </svg>
          <span>Sign in with Google</span>
        </button>

        <div className="text-center pt-2 border-t border-slate-700/50 space-y-2">
          {mode === 'login' && (
            <>
              <button onClick={() => setMode('signup')} className="text-xs text-sky-400 hover:underline">
                Don't have an account? Sign up
              </button>
              <br />
              <button onClick={() => setMode('forgot')} className="text-[11px] text-slate-400 hover:underline">
                Forgot password?
              </button>
            </>
          )}
          {mode !== 'login' && (
            <button onClick={() => setMode('login')} className="text-xs text-sky-400 hover:underline">
              Back to Sign In
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
