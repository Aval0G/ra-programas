import React, { useState, useEffect } from 'react';
import { View, Text, Button, Alert, StyleSheet } from 'react-native';
import { Camera } from 'expo-camera'; // Importar Camera desde expo-camera
import { useRouter } from 'expo-router';

export default function Scan() {
  const [hasPermission, setHasPermission] = useState<boolean | null>(null); 
  const [scanned, setScanned] = useState(false);
  const [type, setType] = useState(Camera.Constants.Type.back); // Usar tipo de cámara (trasera por defecto)
  const router = useRouter();

  useEffect(() => {
    (async () => {
      const { status } = await Camera.requestCameraPermissionsAsync(); // Solicitar permisos de cámara
      setHasPermission(status === 'granted');
    })();
  }, []);

  const handleBarCodeScanned = ({ data }: { data: string }) => { // Especificar tipo de 'data'
    setScanned(true);
    Alert.alert(`Código Escaneado`, `Datos: ${data}`);
  };

  if (hasPermission === null) {
    return <Text>Solicitando permiso de cámara...</Text>;
  }
  if (hasPermission === false) {
    return <Text>No se tiene acceso a la cámara</Text>;
  }

  return (
    <View style={styles.container}>
      <Camera
        style={styles.camera}
        type={type}
        onBarCodeScanned={scanned ? undefined : handleBarCodeScanned} // Detectar código QR
      />
      {scanned && <Button title="Escanear de nuevo" onPress={() => setScanned(false)} />}
      <Button title="Volver" onPress={() => router.back()} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center' },
  camera: { flex: 1 },
});
