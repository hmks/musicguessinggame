import React, { useMemo, useState } from 'react';
import { SafeAreaView, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
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

export default function App() {
  const apiBaseUrl = useMemo(() => resolveBaseUrl(), []);
  const [status, setStatus] = useState('Hazır');

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

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.card}>
        <Text style={styles.title}>MusiGuess</Text>
        <Text style={styles.label}>API Base URL</Text>
        <Text style={styles.value}>{apiBaseUrl}</Text>
        <TouchableOpacity style={styles.button} onPress={checkHealth}>
          <Text style={styles.buttonText}>Kontrol Et</Text>
        </TouchableOpacity>
        <Text style={styles.status}>{status}</Text>
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
    padding: 24,
  },
  card: {
    width: '100%',
    backgroundColor: '#111827',
    borderRadius: 16,
    padding: 24,
    gap: 12,
  },
  title: {
    color: '#f8fafc',
    fontSize: 24,
    fontWeight: '700',
  },
  label: {
    color: '#94a3b8',
    fontSize: 14,
  },
  value: {
    color: '#e2e8f0',
    fontSize: 16,
  },
  button: {
    backgroundColor: '#38bdf8',
    paddingVertical: 12,
    borderRadius: 12,
    alignItems: 'center',
  },
  buttonText: {
    color: '#0f172a',
    fontWeight: '700',
  },
  status: {
    color: '#f8fafc',
    fontSize: 16,
  },
});
