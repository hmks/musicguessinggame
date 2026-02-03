import React, { useMemo, useState } from 'react';
import {
  SafeAreaView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from 'react-native';
import Constants from 'expo-constants';

function resolveBaseUrl() {
  const envBase = process.env.EXPO_PUBLIC_API_BASE_URL;
  if (envBase) {
    return envBase;
  }

  const hostUri =
    Constants.expoConfig?.hostUri ||
    Constants.manifest2?.extra?.expoClient?.hostUri ||
    Constants.manifest?.hostUri;

  if (hostUri) {
    const host = hostUri.split(':')[0];
    return `http://${host}:8001`;
  }

  return 'http://localhost:8001';
}

function buildIdentifierPayload(identifier) {
  if (identifier.includes('@')) {
    return { email: identifier };
  }
  return { username: identifier };
}

export default function App() {
  const apiBaseUrl = useMemo(() => resolveBaseUrl(), []);
  const [identifier, setIdentifier] = useState('');
  const [password, setPassword] = useState('');
  const [token, setToken] = useState(null);
  const [authMode, setAuthMode] = useState('login');
  const [status, setStatus] = useState('Hazır');
  const [gameId, setGameId] = useState(null);
  const [prompt, setPrompt] = useState(null);
  const [guess, setGuess] = useState('');
  const [score, setScore] = useState(0);
  const [round, setRound] = useState(0);
  const [totalRounds, setTotalRounds] = useState(0);

  const checkHealth = async () => {
    setStatus('Kontrol ediliyor...');
    try {
      const response = await fetch(`${apiBaseUrl}/health`);
      const data = await response.json();
      setStatus(`Durum: ${data.status}`);
    } catch (error) {
      setStatus('Hata: API erişilemiyor');
    }
  };

  const submitAuth = async () => {
    setStatus('Yetkilendirme...');
    try {
      const payload = { ...buildIdentifierPayload(identifier), password };
      const endpoint = authMode === 'login' ? 'login' : 'register';
      const response = await fetch(`${apiBaseUrl}/auth/${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorText = await response.text();
        setStatus(`Auth hata: ${errorText}`);
        return;
      }

      if (authMode === 'register') {
        setStatus('Kayıt başarılı. Giriş yapabilirsiniz.');
        setAuthMode('login');
        return;
      }

      const data = await response.json();
      setToken(data.access_token);
      setStatus('Giriş başarılı');
    } catch (error) {
      setStatus('Auth hata: bağlantı sorunu');
    }
  };

  const startGame = async () => {
    setStatus('Oyun başlatılıyor...');
    try {
      const response = await fetch(`${apiBaseUrl}/games/start`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({ count: 3 }),
      });
      if (!response.ok) {
        const errorText = await response.text();
        setStatus(`Oyun hata: ${errorText}`);
        return;
      }
      const data = await response.json();
      setGameId(data.game_id);
      setPrompt(data.song);
      setScore(data.score);
      setRound(data.round);
      setTotalRounds(data.total_rounds);
      setGuess('');
      setStatus('Oyun başladı');
    } catch (error) {
      setStatus('Oyun hata: bağlantı sorunu');
    }
  };

  const submitGuess = async () => {
    if (!gameId) return;
    setStatus('Tahmin gönderiliyor...');
    try {
      const response = await fetch(`${apiBaseUrl}/games/${gameId}/guess`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({ guess }),
      });
      const data = await response.json();
      if (!response.ok) {
        setStatus(`Tahmin hata: ${data.detail || 'Bilinmeyen hata'}`);
        return;
      }
      setScore(data.score);
      setRound(data.round);
      setTotalRounds(data.total_rounds);
      if (data.finished) {
        setPrompt(null);
        setStatus(`Oyun bitti. Skor: ${data.score}`);
      } else {
        setPrompt(data.next_song);
        setStatus(data.correct ? 'Doğru!' : `Yanlış. Doğru: ${data.correct_title}`);
      }
      setGuess('');
    } catch (error) {
      setStatus('Tahmin hata: bağlantı sorunu');
    }
  };

  const logout = () => {
    setToken(null);
    setGameId(null);
    setPrompt(null);
    setScore(0);
    setRound(0);
    setTotalRounds(0);
    setStatus('Çıkış yapıldı');
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.card}>
        <Text style={styles.title}>MusiGuess</Text>
        <Text style={styles.label}>API Base URL</Text>
        <Text style={styles.value}>{apiBaseUrl}</Text>
        <Text style={styles.note}>Android Emulator: http://10.0.2.2:8001</Text>
        <TouchableOpacity style={styles.secondaryButton} onPress={checkHealth}>
          <Text style={styles.secondaryButtonText}>Health Kontrol Et</Text>
        </TouchableOpacity>
        <Text style={styles.status}>{status}</Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.sectionTitle}>Auth</Text>
        <TextInput
          style={styles.input}
          placeholder="Email veya kullanıcı adı"
          placeholderTextColor="#94a3b8"
          value={identifier}
          autoCapitalize="none"
          onChangeText={setIdentifier}
        />
        <TextInput
          style={styles.input}
          placeholder="Şifre"
          placeholderTextColor="#94a3b8"
          value={password}
          secureTextEntry
          onChangeText={setPassword}
        />
        <TouchableOpacity style={styles.button} onPress={submitAuth}>
          <Text style={styles.buttonText}>{authMode === 'login' ? 'Giriş Yap' : 'Kayıt Ol'}</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.linkButton}
          onPress={() => setAuthMode(authMode === 'login' ? 'register' : 'login')}
        >
          <Text style={styles.linkText}>
            {authMode === 'login' ? 'Hesabın yok mu? Kayıt ol' : 'Zaten hesabın var mı? Giriş yap'}
          </Text>
        </TouchableOpacity>
        {token ? (
          <TouchableOpacity style={styles.secondaryButton} onPress={logout}>
            <Text style={styles.secondaryButtonText}>Çıkış Yap</Text>
          </TouchableOpacity>
        ) : null}
      </View>

      <View style={styles.card}>
        <Text style={styles.sectionTitle}>Oyun</Text>
        <Text style={styles.status}>Skor: {score}</Text>
        <Text style={styles.status}>Tur: {round}/{totalRounds || '-'}</Text>
        {prompt ? (
          <View style={styles.promptBox}>
            <Text style={styles.label}>Sanatçı</Text>
            <Text style={styles.value}>{prompt.artist}</Text>
            {prompt.year ? <Text style={styles.note}>Yıl: {prompt.year}</Text> : null}
          </View>
        ) : (
          <Text style={styles.note}>Oyun başlatmak için butona basın.</Text>
        )}
        <TouchableOpacity style={styles.button} onPress={startGame}>
          <Text style={styles.buttonText}>Oyunu Başlat</Text>
        </TouchableOpacity>
        <TextInput
          style={styles.input}
          placeholder="Şarkı tahmini"
          placeholderTextColor="#94a3b8"
          value={guess}
          onChangeText={setGuess}
        />
        <TouchableOpacity style={styles.button} onPress={submitGuess}>
          <Text style={styles.buttonText}>Tahmin Gönder</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0f172a',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 16,
    gap: 12,
  },
  card: {
    width: '100%',
    backgroundColor: '#111827',
    borderRadius: 16,
    padding: 16,
    gap: 10,
  },
  title: {
    color: '#f8fafc',
    fontSize: 24,
    fontWeight: '700',
  },
  sectionTitle: {
    color: '#f8fafc',
    fontSize: 18,
    fontWeight: '600',
  },
  label: {
    color: '#94a3b8',
    fontSize: 14,
  },
  value: {
    color: '#e2e8f0',
    fontSize: 16,
  },
  note: {
    color: '#94a3b8',
    fontSize: 12,
  },
  button: {
    backgroundColor: '#38bdf8',
    paddingVertical: 10,
    borderRadius: 12,
    alignItems: 'center',
  },
  buttonText: {
    color: '#0f172a',
    fontWeight: '700',
  },
  secondaryButton: {
    backgroundColor: '#1f2937',
    paddingVertical: 8,
    borderRadius: 10,
    alignItems: 'center',
  },
  secondaryButtonText: {
    color: '#e2e8f0',
  },
  linkButton: {
    alignItems: 'center',
  },
  linkText: {
    color: '#38bdf8',
  },
  input: {
    backgroundColor: '#0f172a',
    color: '#f8fafc',
    padding: 10,
    borderRadius: 10,
  },
  status: {
    color: '#f8fafc',
    fontSize: 14,
  },
  promptBox: {
    backgroundColor: '#0f172a',
    padding: 12,
    borderRadius: 12,
    gap: 4,
  },
});
