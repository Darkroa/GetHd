import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

const API = 'http://localhost:8000'

interface MasterSeed {
  id: number
  name: string
  created_at: string
}

interface BotWallet {
  id: number
  name: string
  master_seed_id: number | null
  btc_address: string | null
  eth_address: string | null
  created_at: string
}

function App() {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'))
  const [loginUser, setLoginUser] = useState('admin')
  const [loginPass, setLoginPass] = useState('')
  const [loginError, setLoginError] = useState('')

  const [seeds, setSeeds] = useState<MasterSeed[]>([])
  const [wallets, setWallets] = useState<BotWallet[]>([])

  const [newSeedName, setNewSeedName] = useState('')
  const [seedMsg, setSeedMsg] = useState<{ text: string; mnemonic?: string } | null>(null)

  const [botName, setBotName] = useState('')
  const [botSeed, setBotSeed] = useState('')
  const [botMsg, setBotMsg] = useState('')

  const [loading, setLoading] = useState(false)

  const authHeaders = { headers: { Authorization: `Bearer ${token}` } }

  async function login(e: React.FormEvent) {
    e.preventDefault()
    setLoginError('')
    try {
      const form = new FormData()
      form.append('username', loginUser)
      form.append('password', loginPass)
      const res = await axios.post(`${API}/auth/login`, form)
      localStorage.setItem('token', res.data.access_token)
      setToken(res.data.access_token)
    } catch {
      setLoginError('Invalid credentials')
    }
  }

  function logout() {
    localStorage.removeItem('token')
    setToken(null)
  }

  async function fetchData() {
    try {
      const [s] = await Promise.all([
        axios.get(`${API}/api/seeds`, authHeaders),
      ])
      setSeeds(s.data)
    } catch {
      // token may be expired
    }
    try {
      const w = await axios.get(`${API}/api/wallets`, authHeaders)
      setWallets(w.data)
    } catch {
      // endpoint may not exist yet
    }
  }

  useEffect(() => {
    if (token) fetchData()
  }, [token])

  async function createSeed(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setSeedMsg(null)
    try {
      const form = new FormData()
      form.append('name', newSeedName)
      const res = await axios.post(`${API}/api/master-seed`, form, authHeaders)
      setSeedMsg({ text: `Seed "${res.data.name}" created! Save this mnemonic — it won't be shown again:`, mnemonic: res.data.mnemonic })
      setNewSeedName('')
      fetchData()
    } catch (err: any) {
      setSeedMsg({ text: err.response?.data?.detail || 'Error creating seed' })
    }
    setLoading(false)
  }

  async function createBot(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setBotMsg('')
    try {
      const form = new FormData()
      form.append('master_seed_name', botSeed)
      form.append('bot_name', botName)
      await axios.post(`${API}/api/bot-wallet`, form, authHeaders)
      setBotMsg(`Bot wallet "${botName}" created!`)
      setBotName('')
      fetchData()
    } catch (err: any) {
      setBotMsg(err.response?.data?.detail || 'Error creating bot wallet')
    }
    setLoading(false)
  }

  if (!token) {
    return (
      <div className="login-wrap">
        <div className="login-card">
          <div className="brand">🔑 HD Wallet Dashboard</div>
          <form onSubmit={login} className="login-form">
            <label>Username
              <input value={loginUser} onChange={e => setLoginUser(e.target.value)} required />
            </label>
            <label>Password
              <input type="password" value={loginPass} onChange={e => setLoginPass(e.target.value)} required />
            </label>
            {loginError && <p className="error">{loginError}</p>}
            <button type="submit" className="btn-primary">Login</button>
          </form>
          <p className="hint">Default: admin / admin123</p>
        </div>
      </div>
    )
  }

  return (
    <div className="dashboard">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-brand">🔑 HD Wallet</div>
        <nav>
          <a href="#seeds" className="nav-item active">Master Seeds</a>
          <a href="#wallets" className="nav-item">Bot Wallets</a>
        </nav>
        <button className="btn-logout" onClick={logout}>Logout</button>
      </aside>

      {/* Main content */}
      <main className="content">
        <header className="top-bar">
          <h1>HD Wallet Dashboard</h1>
          <span className="badge">{seeds.length} seeds · {wallets.length} wallets</span>
        </header>

        {/* Master Seeds */}
        <section id="seeds" className="panel">
          <h2>Master Seeds</h2>
          <form onSubmit={createSeed} className="inline-form">
            <input
              placeholder="Seed name"
              value={newSeedName}
              onChange={e => setNewSeedName(e.target.value)}
              required
            />
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Creating…' : '+ Create Seed'}
            </button>
          </form>

          {seedMsg && (
            <div className={`msg-box ${seedMsg.mnemonic ? 'success' : 'error'}`}>
              <p>{seedMsg.text}</p>
              {seedMsg.mnemonic && <code className="mnemonic">{seedMsg.mnemonic}</code>}
            </div>
          )}

          <table className="data-table">
            <thead>
              <tr><th>#</th><th>Name</th><th>Created</th></tr>
            </thead>
            <tbody>
              {seeds.length === 0
                ? <tr><td colSpan={3} className="empty">No seeds yet</td></tr>
                : seeds.map(s => (
                  <tr key={s.id}>
                    <td>{s.id}</td>
                    <td>{s.name}</td>
                    <td>{new Date(s.created_at).toLocaleString()}</td>
                  </tr>
                ))
              }
            </tbody>
          </table>
        </section>

        {/* Bot Wallets */}
        <section id="wallets" className="panel">
          <h2>Bot Wallets</h2>
          <form onSubmit={createBot} className="inline-form">
            <input
              placeholder="Bot name"
              value={botName}
              onChange={e => setBotName(e.target.value)}
              required
            />
            <select value={botSeed} onChange={e => setBotSeed(e.target.value)} required>
              <option value="">Select master seed</option>
              {seeds.map(s => <option key={s.id} value={s.name}>{s.name}</option>)}
            </select>
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Creating…' : '+ Create Bot'}
            </button>
          </form>

          {botMsg && <div className={`msg-box ${botMsg.includes('Error') ? 'error' : 'success'}`}><p>{botMsg}</p></div>}

          <table className="data-table">
            <thead>
              <tr><th>#</th><th>Name</th><th>BTC</th><th>ETH</th><th>Created</th></tr>
            </thead>
            <tbody>
              {wallets.length === 0
                ? <tr><td colSpan={5} className="empty">No bot wallets yet</td></tr>
                : wallets.map(w => (
                  <tr key={w.id}>
                    <td>{w.id}</td>
                    <td>{w.name}</td>
                    <td><code>{w.btc_address || '—'}</code></td>
                    <td><code>{w.eth_address || '—'}</code></td>
                    <td>{new Date(w.created_at).toLocaleString()}</td>
                  </tr>
                ))
              }
            </tbody>
          </table>
        </section>
      </main>
    </div>
  )
}

export default App
